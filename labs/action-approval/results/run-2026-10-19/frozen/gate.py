"""Approval binding for one disposable file; trusted-host API, not user authentication."""

import hashlib, json, os, re, tempfile
from pathlib import Path


class Rejected(Exception):
    pass


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(proposal):
    if not isinstance(proposal, dict) or set(proposal) != {
        "target",
        "before_sha256",
        "content",
    }:
        raise Rejected("Invalid proposal fields")
    if proposal["target"] != "plan.txt":
        raise Rejected("Target is outside the one-file allowlist")
    if (
        not isinstance(proposal["content"], str)
        or len(proposal["content"].encode()) > 10000
    ):
        raise Rejected("Invalid content")
    if not isinstance(proposal["before_sha256"], str) or not re.fullmatch(
        "[0-9a-f]{64}", proposal["before_sha256"]
    ):
        raise Rejected("Invalid before hash")
    return sha(json.dumps(proposal, sort_keys=True, separators=(",", ":")).encode())


class Gate:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.approved = set()
        self.applied = set()

    def approve(self, proposal):
        """Call only from the trusted review path; never expose as a model tool."""
        identity = digest(proposal)
        self.approved.add(identity)
        return identity

    def apply(self, proposal):
        identity = digest(proposal)
        if identity not in self.approved:
            raise Rejected("Exact proposal has not been approved")
        target = self.root / "plan.txt"
        if target.is_symlink() or not target.is_file():
            raise Rejected("Target must be an existing regular file, not a symlink")
        current = sha(target.read_bytes())
        replacement = proposal["content"].encode()
        if identity in self.applied and current == sha(replacement):
            return "already_applied"
        if current != proposal["before_sha256"]:
            raise Rejected("Target changed after proposal; review again")
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=self.root, delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(replacement)
            os.replace(temporary, target)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        self.applied.add(identity)
        return "applied"

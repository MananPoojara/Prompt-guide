"""Versioned application memory. No model calls, credentials, or implicit truth judgments."""

import datetime
import re
import sqlite3


class Conflict(Exception):
    """The caller's expected revision is stale."""


def date(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("Use a YYYY-MM-DD date")
    return datetime.date.fromisoformat(value)


def text(value, name):
    if not isinstance(value, str) or not value.strip() or len(value) > 2000:
        raise ValueError(f"{name} must be nonempty text of at most 2000 characters")


class Store:
    def __init__(self, path, namespace):
        text(namespace, "namespace")
        self.namespace = namespace
        self.db = sqlite3.connect(path, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute("""CREATE TABLE IF NOT EXISTS facts (
            namespace TEXT NOT NULL, fact_key TEXT NOT NULL, revision INTEGER NOT NULL,
            value TEXT, source TEXT NOT NULL, observed TEXT NOT NULL, expires TEXT,
            retracted INTEGER NOT NULL, PRIMARY KEY(namespace, fact_key, revision))""")

    def close(self):
        self.db.close()

    def put(self, key, value, source, observed, expires, expected_revision):
        text(value, "value")
        return self._append(
            key, value, source, observed, expires, expected_revision, False
        )

    def retract(self, key, source, observed, expected_revision):
        return self._append(key, None, source, observed, None, expected_revision, True)

    def _append(self, key, value, source, observed, expires, expected, retracted):
        text(key, "key")
        text(source, "source")
        observed_date = date(observed)
        if expires is not None and date(expires) <= observed_date:
            raise ValueError(
                "Expiry must be after observation; expiry date is exclusive"
            )
        if type(expected) is not int or expected < 0:
            raise ValueError("Expected revision must be a nonnegative integer")
        self.db.execute("BEGIN IMMEDIATE")
        try:
            previous = self.db.execute(
                "SELECT revision, observed FROM facts WHERE namespace=? AND fact_key=? ORDER BY revision DESC LIMIT 1",
                (self.namespace, key),
            ).fetchone()
            latest = previous["revision"] if previous else 0
            if latest != expected:
                raise Conflict(
                    f"Expected revision {expected}; current revision is {latest}"
                )
            if previous and observed < previous["observed"]:
                raise ValueError(
                    "Cannot backdate an update before the previous observation"
                )
            revision = latest + 1
            self.db.execute(
                "INSERT INTO facts VALUES (?,?,?,?,?,?,?,?)",
                (
                    self.namespace,
                    key,
                    revision,
                    value,
                    source,
                    observed,
                    expires,
                    int(retracted),
                ),
            )
            self.db.execute("COMMIT")
            return revision
        except Exception:
            self.db.execute("ROLLBACK")
            raise

    def get(self, key, as_of):
        text(key, "key")
        date(as_of)
        row = self.db.execute(
            "SELECT * FROM facts WHERE namespace=? AND fact_key=? AND observed<=? ORDER BY revision DESC LIMIT 1",
            (self.namespace, key, as_of),
        ).fetchone()
        if row is None:
            return {
                "status": "missing",
                "value": None,
                "revision": None,
                "source": None,
            }
        result = {
            "status": "current",
            "value": row["value"],
            "revision": row["revision"],
            "source": row["source"],
        }
        if row["retracted"]:
            result.update(status="retracted", value=None)
        elif row["expires"] is not None and as_of >= row["expires"]:
            result.update(status="expired", value=None)
        return result

    def history(self, key):
        text(key, "key")
        return [
            dict(row)
            for row in self.db.execute(
                "SELECT * FROM facts WHERE namespace=? AND fact_key=? ORDER BY revision",
                (self.namespace, key),
            )
        ]

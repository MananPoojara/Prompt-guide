# Run a real local MCP connection

[Handbook explanation](../../handbook/06-tools-and-mcp.md) · [Start](../../START-HERE.md)

This example launches a real MCP server subprocess, discovers its tool, and calls it. It uses two fictional notes held in memory. **No language model is called.** It needs Python 3.10 or newer and the pinned SDK dependency. The recorded run used Python 3.10.12 and `mcp==2.3.0` on Linux.

## Files

- [server.py](server.py): defines and serves `read_note` over stdio.
- [client.py](client.py): launches the server, discovers the tool, and checks success/error behavior.
- [requirements.txt](requirements.txt): pins the direct SDK dependency; transitive dependencies are not locked.
- [recorded-output.json](recorded-output.json): actual successful stdout from the run on 2026-10-19.
- [recorded-stderr.txt](recorded-stderr.txt): diagnostic output from deliberate error cases.

## Setup and run

From the repository root, on a Unix-like shell:

```bash
python3 -m venv /tmp/prompt-guide-mcp-venv
/tmp/prompt-guide-mcp-venv/bin/python -m pip install -r examples/mcp-notes/requirements.txt
/tmp/prompt-guide-mcp-venv/bin/python examples/mcp-notes/client.py
```

Use a fresh environment path if that directory already contains an unrelated environment. On systems where `venv` is unavailable, `uv` can create the environment without the system's `ensurepip` support:

```bash
uv venv /tmp/prompt-guide-mcp-venv
uv pip install --python /tmp/prompt-guide-mcp-venv/bin/python -r examples/mcp-notes/requirements.txt
/tmp/prompt-guide-mcp-venv/bin/python examples/mcp-notes/client.py
```

Dependency installation requires internet access. Once installed, this example's tool calls use local subprocess communication and in-memory notes. No API key is required. The server is launched by the client; do not start it separately for this example.

Our recording used an isolated temporary dependency directory because system `venv` lacked `ensurepip`:

```bash
python3 -m pip install --target /tmp/prompt-guide-mcp-deps 'mcp==2.3.0'
PYTHONPATH=/tmp/prompt-guide-mcp-deps python3 examples/mcp-notes/client.py
```

A second execution in a clean `uv` environment using Python 3.12.13 also passed all five checks. The standard `venv` route was not available on the recording host; other operating systems were not tested.

## Read the output

The recorded output reports SDK version `2.3.0` and protocol version `2026-07-28`. It contains the advertised input schema and the retrieved dashboard note. The client checks five properties:

1. Exactly the expected tool is advertised.
2. Its input schema requires `note_id`.
3. A valid lookup succeeds and returns the expected record ID.
4. An unknown note returns a tool error.
5. An omitted required argument returns an error.

The deliberately invalid calls can produce diagnostics on stderr. Exit status zero and `checks_passed: 5` indicate that the assertions completed. The exact schema formatting may change with dependencies; the checked behaviors are explicit in the client.

This is protocol integration evidence. It does not test a model choosing the tool or answering the user's question. To add a model later, a host would expose the tool schema, execute permitted model-requested calls, and send results back to the model. That additional loop is explained in the [harness chapter](../../handbook/07-harnesses-and-loops.md).

The SDK version 2 API differs from older tutorials using `FastMCP` and manual `ClientSession` setup. Keep this example's imports and pinned version together. [Official SDK client documentation](https://py.sdk.modelcontextprotocol.io/client/).

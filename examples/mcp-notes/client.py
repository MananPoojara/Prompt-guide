"""Exercise a real MCP subprocess without calling a language model."""
import asyncio
import json
import os
from pathlib import Path
import sys
from importlib.metadata import version
from mcp import Client
from mcp.client.stdio import StdioServerParameters

async def main():
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).with_name("server.py"))],
        env=dict(os.environ),
    )
    async with Client(params) as client:
        listed = await client.list_tools()
        assert [tool.name for tool in listed.tools] == ["read_note"]
        schema = listed.tools[0].input_schema
        assert "note_id" in schema["required"]
        good = await client.call_tool("read_note", {"note_id": "dashboard"})
        assert not good.is_error
        assert good.structured_content["id"] == "dashboard"
        missing = await client.call_tool("read_note", {"note_id": "unknown"})
        assert missing.is_error
        invalid = await client.call_tool("read_note", {})
        assert invalid.is_error
        print(json.dumps({
            "sdk_version": version("mcp"),
            "protocol_version": client.protocol_version,
            "tools": [{"name": t.name, "input_schema": t.input_schema} for t in listed.tools],
            "successful_result": good.structured_content,
            "unknown_note_is_error": missing.is_error,
            "missing_argument_is_error": invalid.is_error,
            "checks_passed": 5,
            "model_called": False,
        }, indent=2))

if __name__ == "__main__":
    asyncio.run(main())

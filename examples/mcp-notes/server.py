"""A read-only MCP server over a deliberately small, fictional notes collection."""
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

server = MCPServer("Prompt Guide notes")
NOTES = {
    "search-fix": {"id": "search-fix", "text": "Priya will fix search by 2026-11-03."},
    "dashboard": {"id": "dashboard", "text": "Alex proposed 2026-11-05. No one accepted ownership or a deadline."},
}

@server.tool()
def read_note(note_id: str) -> dict[str, str]:
    """Read a fictional project note by exact ID: search-fix or dashboard."""
    if note_id not in NOTES:
        raise ToolError(f"Unknown note ID: {note_id}")
    return dict(NOTES[note_id])

if __name__ == "__main__":
    server.run(transport="stdio")

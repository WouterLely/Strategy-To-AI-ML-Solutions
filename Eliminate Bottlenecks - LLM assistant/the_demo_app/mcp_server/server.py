<<<<<<< HEAD
from fastmcp import FastMCP


mcp = FastMCP("demo-mcp")


@mcp.tool()
def echo(text: str) -> str:
    """Echo the provided text."""
    return text


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b


if __name__ == "__main__":
    # Runs an MCP server that can be discovered by compatible clients.
    # For container usage, run `python -m mcp_server.server`.
    mcp.run()



=======
from fastmcp import FastMCP


mcp = FastMCP("demo-mcp")


@mcp.tool()
def echo(text: str) -> str:
    """Echo the provided text."""
    return text


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b


if __name__ == "__main__":
    # Runs an MCP server that can be discovered by compatible clients.
    # For container usage, run `python -m mcp_server.server`.
    mcp.run()



>>>>>>> 90fd3198baf6326b2fee62bdd5459fd732dfde2c

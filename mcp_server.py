"""
Your MCP server. ← UNIT 4, MILESTONE 1

Right now your tools only exist inside your own program. Nothing else can reach
them. MCP is an agreed shape you wrap a tool in so that anything speaking the
same protocol can call it — your agent today, a different agent tomorrow,
someone else's app after that.

**You're moving one tool. Not three.** The point is to see the seam.
`search_listings` is the one to move: it doesn't call the model, so nothing is
slow and nothing changes between runs while you're learning the shape.

    python mcp_server.py        starts the server (it will just sit there — that's right)
    python mcp_client.py        asks the server what it offers
"""

from mcp.server.fastmcp import FastMCP

from tools import search_listings as _search_listings_impl  # noqa: F401 — you'll use this below

# log_level="WARNING" keeps the server from printing an INFO line for every request.
mcp = FastMCP("fitfindr", log_level="WARNING")


@mcp.tool()
def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search clothing catalog listings based on a text description, optional size filter, and maximum price in whole dollars.
    Returns a list of matching listing dictionaries, or an empty list if no items match the criteria.
    """
    return _search_listings_impl(description, size, max_price)


if __name__ == "__main__":
    mcp.run()

"""
---

### How to test and wire it up:

1. **Save this code** into your `mcp_server.py`
2. **Start the server** in your terminal inside bash python mcp_server.py
"""

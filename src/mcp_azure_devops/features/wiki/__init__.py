"""Azure DevOps Wiki feature package."""
from . import tools

def register(mcp):
    """
    Register wiki components with the MCP server.
    
    Args:
        mcp: The FastMCP server instance
    """
    tools.register_tools(mcp)

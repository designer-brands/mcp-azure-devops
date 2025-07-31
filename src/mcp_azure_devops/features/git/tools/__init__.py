"""
Register all git tools with the MCP server.
"""

from mcp_azure_devops.features.git.tools import pull_requests, repositories


def register_tools(mcp):
    """Register all git tools with the MCP server."""
    repositories.register_tools(mcp)
    pull_requests.register_tools(mcp)

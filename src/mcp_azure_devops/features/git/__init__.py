"""
Azure DevOps Git Features
"""

from mcp_azure_devops.features.git import tools


def register(mcp):
    """
    Register all git features with the MCP server.
    """
    tools.register_tools(mcp)

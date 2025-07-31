"""
Exposes Azure DevOps pipelines features
"""

from mcp_azure_devops.features.pipelines import tools


def register(mcp):
    """Register all pipelines components with the MCP server."""
    tools.register_tools(mcp)

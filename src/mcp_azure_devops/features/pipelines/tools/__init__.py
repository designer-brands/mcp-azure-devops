"""
Tools for Azure DevOps pipelines
"""

from . import pipelines


def register_tools(mcp):
    """Register all pipelines tools with the MCP server."""
    pipelines.register_tools(mcp)

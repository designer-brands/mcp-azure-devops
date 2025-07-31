# Azure DevOps MCP features package
from mcp_azure_devops.features import git, projects, teams, wiki, work_items


def register_all(mcp):
    """
    Register all features with the MCP server.

    Args:
        mcp: The FastMCP server instance
    """
    work_items.register(mcp)
    projects.register(mcp)
    teams.register(mcp)
    wiki.register(mcp)
    git.register(mcp)

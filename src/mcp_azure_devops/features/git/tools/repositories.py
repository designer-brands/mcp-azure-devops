"""
Tools for Azure DevOps Git repositories
"""

from mcp_azure_devops.features.git.common import (
    AzureDevOpsClientError,
    get_git_client,
)


def _format_repository(repo):
    """Formats a repository for display."""
    return f"""\
# {repo.name}
- **ID**: {repo.id}
- **Default Branch**: {repo.default_branch}
- **URL**: {repo.web_url}
"""


def _list_repositories_impl(git_client, project):
    """Implementation of listing repositories."""
    repos = git_client.get_repositories(project=project)

    if not repos:
        return f"No repositories found in project {project}."

    formatted_repos = []
    for repo in repos:
        formatted_repos.append(_format_repository(repo))

    return "\n\n".join(formatted_repos)


def register_tools(mcp):
    """Register repository tools with the MCP server."""

    @mcp.tool()
    def list_repositories(project: str):
        """
        Lists all Git repositories in a project.

        Use this tool when you need to:
        - View all repositories in a project
        - Find a specific repository by name
        - Get repository IDs for use in other operations

        Args:
            project: Project name or ID

        Returns:
            Formatted string listing all repositories with names, IDs, and URLs
        """
        try:
            git_client = get_git_client()
            return _list_repositories_impl(git_client, project)
        except AzureDevOpsClientError as e:
            return f"Error: {str(e)}"

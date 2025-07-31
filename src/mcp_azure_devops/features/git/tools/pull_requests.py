
"""
Tools for Azure DevOps Git pull requests
"""


from mcp_azure_devops.features.git.common import (
    AzureDevOpsClientError,
    get_git_client,
)


def _format_pull_request(pr):
    """Formats a pull request for display."""
    return f"""\
# {pr.title}
- **ID**: {pr.pull_request_id}
- **Status**: {pr.status}
- **Source Branch**: {pr.source_ref_name}
- **Target Branch**: {pr.target_ref_name}
- **URL**: {pr.url}
"""


def _get_pull_requests_impl(git_client, project, repository_id):
    """Implementation of listing pull requests."""
    search_criteria = {"status": "active"}
    prs = git_client.get_pull_requests(
        project=project,
        repository_id=repository_id,
        search_criteria=search_criteria,
    )

    if not prs:
        return f"No active pull requests found in repository {repository_id}."

    formatted_prs = []
    for pr in prs:
        formatted_prs.append(_format_pull_request(pr))

    return "\n\n".join(formatted_prs)


def _create_pull_request_impl(
    git_client,
    project,
    repository_id,
    source_ref_name,
    target_ref_name,
    title,
    description,
):
    """Implementation of creating a pull request."""
    pr = git_client.create_pull_request(
        project=project,
        repository_id=repository_id,
        git_pull_request_to_create={
            "source_ref_name": source_ref_name,
            "target_ref_name": target_ref_name,
            "title": title,
            "description": description,
        },
    )
    return _format_pull_request(pr)


def register_tools(mcp):
    """Register pull request tools with the MCP server."""

    @mcp.tool()
    def get_pull_requests(project: str, repository_id: str):
        """
        Lists all active pull requests in a repository.

        Use this tool when you need to:
        - View all active pull requests in a repository
        - Find a specific pull request by title
        - Get pull request IDs for use in other operations

        Args:
            project: Project name or ID
            repository_id: Repository name or ID

        Returns:
            Formatted string listing all active pull requests with titles, IDs, and URLs
        """
        try:
            git_client = get_git_client()
            return _get_pull_requests_impl(git_client, project, repository_id)
        except AzureDevOpsClientError as e:
            return f"Error: {str(e)}"

    @mcp.tool()
    def create_pull_request(
        project: str,
        repository_id: str,
        source_ref_name: str,
        target_ref_name: str,
        title: str,
        description: str = None,
    ):
        """
        Creates a new pull request.

        Use this tool when you need to:
        - Create a new pull request
        - Start a code review

        Args:
            project: Project name or ID
            repository_id: Repository name or ID
            source_ref_name: The name of the source branch
            target_ref_name: The name of the target branch
            title: The title of the pull request
            description: An optional description of the pull request

        Returns:
            Formatted string containing the created pull request details
        """
        try:
            git_client = get_git_client()
            return _create_pull_request_impl(
                git_client,
                project,
                repository_id,
                source_ref_name,
                target_ref_name,
                title,
                description,
            )
        except AzureDevOpsClientError as e:
            return f"Error: {str(e)}"


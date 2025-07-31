"""
Tools for Azure DevOps Pipelines
"""

from mcp_azure_devops.features.pipelines.common import (
    AzureDevOpsClientError,
    get_pipelines_client,
)


def _format_pipeline(pipeline):
    """Formats a pipeline for display."""
    return f"""\
## {pipeline.name}
- **ID**: {pipeline.id}
- **Folder**: {pipeline.folder}
- **Revision**: {pipeline.revision}
- **URL**: {pipeline._links.web.href}
"""


def _list_pipelines_impl(pipelines_client, project):
    """Implementation of listing pipelines."""
    pipelines = pipelines_client.list_pipelines(project=project)

    if not pipelines:
        return f"No pipelines found in project {project}."

    formatted_pipelines = []
    for pipeline in pipelines:
        formatted_pipelines.append(_format_pipeline(pipeline))

    return "\n\n".join(formatted_pipelines)


def _get_pipeline_impl(pipelines_client, project, pipeline_id):
    """Implementation of getting a pipeline."""
    pipeline = pipelines_client.get_pipeline(
        project=project, pipeline_id=pipeline_id
    )
    return _format_pipeline(pipeline)


def register_tools(mcp):
    """Register pipeline tools with the MCP server."""

    @mcp.tool()
    def list_pipelines(project: str):
        """
        Lists all pipelines in a project.

        Use this tool when you need to:
        - View all pipelines in a project
        - Find a specific pipeline by name
        - Get pipeline IDs for use in other operations

        Args:
            project: Project name or ID

        Returns:
            Formatted string listing all pipelines with names, IDs, and URLs
        """
        try:
            pipelines_client = get_pipelines_client()
            return _list_pipelines_impl(pipelines_client, project)
        except AzureDevOpsClientError as e:
            return f"Error: {str(e)}"

    @mcp.tool()
    def get_pipeline(project: str, pipeline_id: int):
        """
        Gets a single pipeline.

        Use this tool when you need to:
        - Get the details of a single pipeline

        Args:
            project: Project name or ID
            pipeline_id: The ID of the pipeline

        Returns:
            Formatted string containing the pipeline details
        """
        try:
            pipelines_client = get_pipelines_client()
            return _get_pipeline_impl(pipelines_client, project, pipeline_id)
        except AzureDevOpsClientError as e:
            return f"Error: {str(e)}"

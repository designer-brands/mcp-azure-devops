"""
Common utilities for Azure DevOps pipelines
"""

from mcp_azure_devops.utils.azure_client import (
    AzureDevOpsClientError,
    get_connection,
)


def get_pipelines_client():
    """Get the Azure DevOps Pipelines client."""
    try:
        connection = get_connection()
        return connection.clients.get_pipelines_client()
    except Exception as e:
        raise AzureDevOpsClientError(f"Failed to get Pipelines client: {str(e)}")

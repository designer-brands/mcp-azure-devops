"""
Common utilities for Azure DevOps Git features.
"""

from azure.devops.v7_1.git import GitClient

from mcp_azure_devops.utils.azure_client import get_connection


class AzureDevOpsClientError(Exception):
    """Exception raised for errors in Azure DevOps client operations."""

    pass


def get_git_client() -> GitClient:
    """
    Get the git client.

    Returns:
        GitClient instance

    Raises:
        AzureDevOpsClientError: If connection or client creation fails
    """
    # Get connection to Azure DevOps
    connection = get_connection()

    if not connection:
        raise AzureDevOpsClientError(
            "Azure DevOps PAT or organization URL not found in "
            "environment variables."
        )

    # Get the git client
    git = connection.clients.get_git_client()

    if git is None:
        raise AzureDevOpsClientError("Failed to get git client.")

    return git

"""
Common utilities for Azure DevOps Git features.

This module provides shared functionality used by both tools and resources.
"""

from azure.devops.v7_1.git import GitClient

from mcp_azure_devops.utils.azure_client import get_connection
from mcp_azure_devops.utils.exceptions import AzureDevOpsClientError


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

    # Get the git client
    git_client = connection.clients.get_git_client()

    if git_client is None:
        raise AzureDevOpsClientError("Failed to get git client.")

    return git_client

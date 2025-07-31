"""
Common utilities for Azure DevOps teams features.

This module provides shared functionality used by both tools and resources.
"""

from azure.devops.v7_1.core import CoreClient
from azure.devops.v7_1.work import WorkClient

from mcp_azure_devops.utils.azure_client import get_connection
from mcp_azure_devops.utils.exceptions import AzureDevOpsClientError


def get_core_client() -> CoreClient:
    """
    Get the core client for Azure DevOps.

    Returns:
        CoreClient instance

    Raises:
        AzureDevOpsClientError: If connection or client creation fails
    """
    # Get connection to Azure DevOps
    connection = get_connection()

    # Get the core client
    core_client = connection.clients.get_core_client()

    if core_client is None:
        raise AzureDevOpsClientError("Failed to get core client.")

    return core_client


def get_work_client() -> WorkClient:
    """
    Get the work client for Azure DevOps.

    Returns:
        WorkClient instance

    Raises:
        AzureDevOpsClientError: If connection or client creation fails
    """
    # Get connection to Azure DevOps
    connection = get_connection()

    # Get the work client
    work_client = connection.clients.get_work_client()

    if work_client is None:
        raise AzureDevOpsClientError("Failed to get work client.")

    return work_client

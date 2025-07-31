"""
Common utilities for Azure DevOps work item features.

This module provides shared functionality used by both tools and resources.
"""

from azure.devops.v7_1.work_item_tracking import WorkItemTrackingClient

from mcp_azure_devops.utils.azure_client import get_connection
from mcp_azure_devops.utils.exceptions import AzureDevOpsClientError


def get_work_item_client() -> WorkItemTrackingClient:
    """
    Get the work item tracking client.

    Returns:
        WorkItemTrackingClient instance

    Raises:
        AzureDevOpsClientError: If connection or client creation fails
    """
    # Get connection to Azure DevOps
    connection = get_connection()

    # Get the work item tracking client
    wit_client = connection.clients.get_work_item_tracking_client()

    if wit_client is None:
        raise AzureDevOpsClientError(
            "Failed to get work item tracking client."
        )

    return wit_client

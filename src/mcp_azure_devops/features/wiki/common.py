"""
Common utilities for Azure DevOps teams features.

This module provides shared functionality used by both tools and resources.
"""

from azure.devops.v7_1.search import SearchClient
from azure.devops.v7_1.wiki import WikiClient

from mcp_azure_devops.utils.azure_client import get_connection
from mcp_azure_devops.utils.exceptions import AzureDevOpsClientError


def get_wiki_client() -> WikiClient:
    """
    Get the wiki client for Azure DevOps.

    Returns:
        WikiClient instance

    Raises:
        AzureDevOpsClientError: If connection or client creation fails
    """
    # Get connection to Azure DevOps
    connection = get_connection()

    # Get the wiki client
    wiki_client = connection.clients.get_wiki_client()

    if wiki_client is None:
        raise AzureDevOpsClientError("Failed to get wiki client.")

    return wiki_client


def get_search_client() -> SearchClient:
    """
    Get the search client for Azure DevOps.

    Returns:
        SearchClient instance

    Raises:
        AzureDevOpsClientError: If connection or client creation fails
    """
    # Get connection to Azure DevOps
    connection = get_connection()

    # Get the wiki client
    search_client = connection.clients.get_search_client()

    if search_client is None:
        raise AzureDevOpsClientError("Failed to get search client.")

    return search_client

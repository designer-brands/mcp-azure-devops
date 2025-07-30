# Helper functions for the wiki feature
from mcp_azure_devops.utils.azure_client import get_connection

class AzureDevOpsClientError(Exception):
    """Custom exception for Azure DevOps client errors."""
    pass

def get_wiki_client():
    """Get the Wiki client."""
    try:
        connection = get_connection()
        return connection.clients.get_wiki_client()
    except Exception as e:
        raise AzureDevOpsClientError(f"Failed to get Wiki client: {str(e)}")

def get_search_client():
    """Get the Search client."""
    try:
        connection = get_connection()
        return connection.clients.get_search_client()
    except Exception as e:
        raise AzureDevOpsClientError(f"Failed to get Search client: {str(e)}")

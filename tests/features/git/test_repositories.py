"""
Tests for Azure DevOps Git features.
"""

from unittest.mock import MagicMock, patch

from mcp_azure_devops.features.git.tools.repositories import (
    _format_repository,
    _list_repositories_impl,
)


def test_format_repository():
    """Test formatting a repository for display."""
    mock_repo = MagicMock()
    mock_repo.name = "Test Repo"
    mock_repo.id = "repo-id-123"
    mock_repo.default_branch = "main"
    mock_repo.web_url = "https://dev.azure.com/org/proj/_git/Test%20Repo"

    result = _format_repository(mock_repo)

    assert "# Test Repo" in result
    assert "- **ID**: repo-id-123" in result
    assert "- **Default Branch**: main" in result
    assert (
        "- **URL**: https://dev.azure.com/org/proj/_git/Test%20Repo" in result
    )


@patch("mcp_azure_devops.features.git.common.get_connection")
def test_list_repositories_impl(mock_get_connection):
    """Test listing repositories."""
    mock_git_client = MagicMock()
    mock_get_connection.return_value.clients.get_git_client.return_value = (
        mock_git_client
    )

    mock_repo1 = MagicMock()
    mock_repo1.name = "Repo 1"
    mock_repo1.id = "1"
    mock_repo1.default_branch = "main"
    mock_repo1.web_url = "http://repo1.com"

    mock_repo2 = MagicMock()
    mock_repo2.name = "Repo 2"
    mock_repo2.id = "2"
    mock_repo2.default_branch = "develop"
    mock_repo2.web_url = "http://repo2.com"

    mock_git_client.get_repositories.return_value = [mock_repo1, mock_repo2]

    result = _list_repositories_impl(mock_git_client, "Test Project")

    assert "# Repo 1" in result
    assert "# Repo 2" in result
    assert "- **ID**: 1" in result
    assert "- **ID**: 2" in result


@patch("mcp_azure_devops.features.git.common.get_connection")
def test_list_repositories_impl_no_repos(mock_get_connection):
    """Test listing repositories when none are found."""
    mock_git_client = MagicMock()
    mock_get_connection.return_value.clients.get_git_client.return_value = (
        mock_git_client
    )
    mock_git_client.get_repositories.return_value = []

    result = _list_repositories_impl(mock_git_client, "Test Project")

    assert "No repositories found in project Test Project." in result

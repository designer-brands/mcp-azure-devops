"""
Tests for the Azure DevOps Git pull request tools.
"""

import unittest
from unittest.mock import MagicMock, patch

from mcp_azure_devops.features.git.tools.pull_requests import (
    _create_pull_request_impl,
    _format_pull_request,
    _get_pull_requests_impl,
)


class TestPullRequests(unittest.TestCase):
    """Tests for the pull request tools."""

    def test_format_pull_request(self):
        """Test the formatting of a pull request."""
        pr = MagicMock()
        pr.title = "Test PR"
        pr.pull_request_id = 123
        pr.status = "active"
        pr.source_ref_name = "features/test"
        pr.target_ref_name = "main"
        pr.url = "http://example.com/pr/123"

        formatted_pr = _format_pull_request(pr)
        self.assertIn("# Test PR", formatted_pr)
        self.assertIn("- **ID**: 123", formatted_pr)
        self.assertIn("- **Status**: active", formatted_pr)

    def test_get_pull_requests_impl_found(self):
        """Test getting pull requests when some are found."""
        git_client = MagicMock()
        pr = MagicMock()
        pr.title = "Test PR"
        pr.pull_request_id = 123
        pr.status = "active"
        pr.source_ref_name = "features/test"
        pr.target_ref_name = "main"
        pr.url = "http://example.com/pr/123"
        git_client.get_pull_requests.return_value = [pr]

        result = _get_pull_requests_impl(git_client, "TestProject", "TestRepo")
        self.assertIn("# Test PR", result)

    def test_get_pull_requests_impl_not_found(self):
        """Test getting pull requests when none are found."""
        git_client = MagicMock()
        git_client.get_pull_requests.return_value = []

        result = _get_pull_requests_impl(git_client, "TestProject", "TestRepo")
        self.assertEqual(
            result, "No active pull requests found in repository TestRepo."
        )

    def test_create_pull_request_impl(self):
        """Test creating a pull request."""
        git_client = MagicMock()
        pr = MagicMock()
        pr.title = "Test PR"
        pr.pull_request_id = 123
        pr.status = "active"
        pr.source_ref_name = "features/test"
        pr.target_ref_name = "main"
        pr.url = "http://example.com/pr/123"
        git_client.create_pull_request.return_value = pr

        result = _create_pull_request_impl(
            git_client,
            "TestProject",
            "TestRepo",
            "features/test",
            "main",
            "Test PR",
            "This is a test PR.",
        )

        self.assertIn("# Test PR", result)
        self.assertIn("- **ID**: 123", result)


if __name__ == "__main__":
    unittest.main()

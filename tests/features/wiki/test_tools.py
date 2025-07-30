# Tests for the wiki tools
import unittest
from unittest.mock import MagicMock

from mcp_azure_devops.features.wiki.tools import (
    _format_page,
    _get_wiki_by_id_impl,
    _get_wiki_by_path_impl,
    _search_wiki_impl,
)


class TestWikiTools(unittest.TestCase):
    def test_search_wiki_impl(self):
        mock_search_client = MagicMock()

        mock_project = MagicMock(id="proj-1")
        mock_project.name = "Test Project"
        mock_wiki = MagicMock(id="wiki-1")
        mock_wiki.name = "Test Wiki"

        mock_search_client.fetch_wiki_search_results.return_value = MagicMock(
            results=[
                MagicMock(
                    file_name="Test Page",
                    project=mock_project,
                    wiki=mock_wiki,
                    path="/Test-Page",
                )
            ]
        )
        result = _search_wiki_impl(mock_search_client, "test")
        self.assertIn("## Wiki Search Results", result)
        self.assertIn("- **Query:** test", result)
        self.assertIn("### Test Page", result)
        self.assertIn("- **Path:** /Test-Page", result)
        self.assertIn("- **Project:** Test Project (proj-1)", result)
        self.assertIn("- **Wiki:** Test Wiki (wiki-1)", result)

    def test_format_page(self):
        mock_page = MagicMock(
            id=1,
            path="/Test-Page",
            order=1,
            url="http://example.com/page",
            content="This is the content.",
            sub_pages=[
                MagicMock(
                    path="/Sub-Page",
                    id=2,
                    order=2,
                    url="http://example.com/sub",
                )
            ],
        )
        result = _format_page(mock_page)
        self.assertIn("---", result)
        self.assertIn("id: 1", result)
        self.assertIn("path: /Test-Page", result)
        self.assertIn("order: 1", result)
        self.assertIn("url: http://example.com/page", result)
        self.assertIn("sub_pages:", result)
        self.assertIn("- path: /Sub-Page", result)
        self.assertIn("  id: 2", result)
        self.assertIn("  order: 2", result)
        self.assertIn("  url: http://example.com/sub", result)
        self.assertIn("This is the content.", result)

    def test_get_wiki_by_path_impl(self):
        mock_wiki_client = MagicMock()
        mock_page = MagicMock(
            page=MagicMock(
                id=1,
                path="/Test-Page",
                order=1,
                url="http://example.com/page",
                content="This is the content of the test page.",
                sub_pages=[],
            )
        )
        mock_wiki_client.get_page.return_value = mock_page
        result = _get_wiki_by_path_impl(
            mock_wiki_client, "TestProject", "TestWiki", "/Test-Page"
        )
        self.assertIn("id: 1", result)
        self.assertIn("path: /Test-Page", result)
        self.assertIn("order: 1", result)
        self.assertIn("url: http://example.com/page", result)
        self.assertIn("This is the content of the test page.", result)

    def test_get_wiki_by_id_impl(self):
        mock_wiki_client = MagicMock()
        mock_page = MagicMock(
            page=MagicMock(
                id=123,
                path="/Test-Page",
                order=1,
                url="http://example.com/page",
                content="This is the content of the test page.",
                sub_pages=[],
            )
        )
        mock_wiki_client.get_page_by_id.return_value = mock_page
        result = _get_wiki_by_id_impl(
            mock_wiki_client, "TestProject", "TestWiki", 123
        )
        self.assertIn("id: 123", result)
        self.assertIn("path: /Test-Page", result)
        self.assertIn("order: 1", result)
        self.assertIn("url: http://example.com/page", result)
        self.assertIn("This is the content of the test page.", result)


if __name__ == "__main__":
    unittest.main()

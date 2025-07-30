# Tests for the wiki tools
import unittest
from unittest.mock import MagicMock

from mcp_azure_devops.features.wiki.tools import (
    _get_wiki_by_id_impl,
    _get_wiki_by_path_impl,
    _search_wiki_impl,
)


class TestWikiTools(unittest.TestCase):
    def test_search_wiki_impl(self):
        mock_search_client = MagicMock()

        mock_hit = MagicMock()
        mock_hit.field_reference_name = "content"
        mock_hit.highlights = ["This is a test page."]

        mock_search_client.fetch_wiki_search_results.return_value = MagicMock(
            results=[
                MagicMock(
                    file_name="Test Page",
                    project=MagicMock(name="Test Project", id="proj-1"),
                    wiki=MagicMock(name="Test Wiki", id="wiki-1"),
                    path="/Test-Page",
                    hits=[mock_hit],
                )
            ]
        )
        result = _search_wiki_impl(mock_search_client, "test")
        self.assertIn("### Test Page", result)
        self.assertIn("- **Content Highlights:**", result)
        self.assertIn("  - **content:** This is a test page.", result)

    def test_get_wiki_by_path_impl(self):
        mock_wiki_client = MagicMock()
        mock_wiki_client.get_page.return_value = MagicMock(
            path="/Test-Page", content="This is the content of the test page."
        )
        result = _get_wiki_by_path_impl(
            mock_wiki_client, "TestWiki", "/Test-Page"
        )
        self.assertIn("# /Test-Page", result)
        self.assertIn("This is the content of the test page.", result)

    def test_get_wiki_by_id_impl(self):
        mock_wiki_client = MagicMock()
        mock_wiki_client.get_page_by_id.return_value = MagicMock(
            path="/Test-Page", content="This is the content of the test page."
        )
        result = _get_wiki_by_id_impl(mock_wiki_client, "TestWiki", 123)
        self.assertIn("# /Test-Page", result)
        self.assertIn("This is the content of the test page.", result)


if __name__ == "__main__":
    unittest.main()

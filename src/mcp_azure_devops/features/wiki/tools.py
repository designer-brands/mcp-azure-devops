# Tools for interacting with the Azure DevOps Wiki
from mcp import Tool

from .common import AzureDevOpsClientError, get_search_client, get_wiki_client


def _search_wiki_impl(search_client, query):
    """Implementation of searching the wiki."""
    search_payload = {"searchText": query, "$top": 500}
    results = search_client.fetch_wiki_search_results(
        search_payload, project=None
    )
    if not results.results:
        return f"No wiki pages found for query: {query}"

    formatted_results = [
        f"""## Wiki Search Results
- **Query:** {query}"""
    ]

    for result in results.results:
        page_details = [
            f"""### {result.file_name}
- **Path:** {result.path}
- **Project:** {result.project.name} ({result.project.id})
- **Wiki:** {result.wiki.name} ({result.wiki.id})"""
        ]

        if hasattr(result, "hits") and result.hits:
            hit_lines = ["- **Content Highlights:**"]
            for hit in result.hits:
                if (
                    hasattr(hit, "field_reference_name")
                    and hasattr(hit, "highlights")
                    and hit.highlights
                ):
                    highlights_str = " ... ".join(hit.highlights)
                    hit_lines.append(
                        f"  - **{hit.field_reference_name}:** {highlights_str}"
                    )

            if len(hit_lines) > 1:
                page_details.append("\n".join(hit_lines))

        formatted_results.append("\n".join(page_details))

    return "\n\n".join(formatted_results)


def _get_wiki_by_path_impl(wiki_client, wiki_id, path):
    """Implementation of getting a wiki page by path."""
    page = wiki_client.get_page(
        wiki_identifier=wiki_id,
        path=path,
        recursion_level="full",
        include_content=True,
    )
    return f"# {page.path}\n{page.content}"


def _get_wiki_by_id_impl(wiki_client, wiki_id, id):
    """Implementation of getting a wiki page by id."""
    page = wiki_client.get_page_by_id(
        wiki_identifier=wiki_id,
        id=id,
        recursion_level="full",
        include_content=True,
    )
    return f"# {page.path}\n{page.content}"


def register_tools(mcp):
    """Register wiki tools with the MCP server."""

    @Tool(mcp=mcp)
    def search_wiki(query: str):
        """Search Azure DevOps Wiki to find related material for a given query.

        Use this tool when you need to:
        - Find wiki pages related to a specific topic
        - Search for documentation within the Azure DevOps wiki
        - Get a list of wiki pages that match a search term

        Args:
            query: The search query to find wiki pages

        Returns:
            A formatted string containing the search results, including the file name, project name and ID, wiki name and ID, and the path to the wiki page.
        """
        try:
            search_client = get_search_client()
            return _search_wiki_impl(search_client, query)
        except AzureDevOpsClientError as e:
            return f"Error: {str(e)}"

    @Tool(mcp=mcp)
    def get_wiki_by_path(wiki_id: str, path: str):
        """Get Azure DevOps Wiki content by path returned from search_wiki.

        Use this tool when you need to:
        - Retrieve the full content of a wiki page when you know its path
        - Read a specific document from the wiki

        Args:
            wiki_id: The ID of the wiki
            path: The path to the wiki page

        Returns:
            The full content of the wiki page as a markdown string.
        """
        try:
            wiki_client = get_wiki_client()
            return _get_wiki_by_path_impl(wiki_client, wiki_id, path)
        except AzureDevOpsClientError as e:
            return f"Error: {str(e)}"

    @Tool(mcp=mcp)
    def get_wiki_by_id(wiki_id: str, id: int):
        """Get Azure DevOps Wiki content by id returned from search_wiki.

        Use this tool when you need to:
        - Retrieve the full content of a wiki page when you know its ID
        - Read a specific document from the wiki using its unique identifier

        Args:
            wiki_id: The ID of the wiki
            id: The ID of the wiki page

        Returns:
            The full content of the wiki page as a markdown string.
        """
        try:
            wiki_client = get_wiki_client()
            return _get_wiki_by_id_impl(wiki_client, wiki_id, id)
        except AzureDevOpsClientError as e:
            return f"Error: {str(e)}"

# Tools for interacting with the Azure DevOps Wiki

from urllib.parse import unquote

from mcp_azure_devops.utils.exceptions import AzureDevOpsClientError

from .common import get_search_client, get_wiki_client


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

        formatted_results.append("\n".join(page_details))

    return "\n\n".join(formatted_results)


def _format_page(page):
    """Formats a wiki page with frontmatter."""
    frontmatter = [
        "---",
        f"id: {getattr(page, 'id', 'N/A')}",
        f"path: {getattr(page, 'path', 'N/A')}",
        f"order: {getattr(page, 'order', 'N/A')}",
        f"url: {getattr(page, 'url', 'N/A')}",
    ]

    if hasattr(page, "sub_pages") and page.sub_pages:
        frontmatter.append("sub_pages:")
        for sub_page in page.sub_pages:
            sub_page_details = [
                f"  - path: {getattr(sub_page, 'path', 'N/A')}",
                f"    id: {getattr(sub_page, 'id', 'N/A')}",
                f"    order: {getattr(sub_page, 'order', 'N/A')}",
                f"    url: {getattr(sub_page, 'url', 'N/A')}",
            ]
            frontmatter.extend(sub_page_details)

    frontmatter.append("---")

    frontmatter_str = "\n".join(frontmatter)
    content = getattr(page, "content", "")

    return f"{frontmatter_str}\n\n{content}"


def _get_wiki_by_path_impl(wiki_client, project, wiki_id, path):
    """Implementation of getting a wiki page by path."""

    # replace - with space and remove .md extension
    correct_path = path.replace("-", " ")
    if correct_path.endswith(".md"):
        correct_path = correct_path[:-3]

    correct_path = unquote(correct_path)

    result = wiki_client.get_page(
        project=project,
        wiki_identifier=wiki_id,
        path=correct_path,
        recursion_level="oneLevel",
        include_content=True,
    )
    return _format_page(result.page)


def _get_wiki_by_id_impl(wiki_client, project, wiki_id, id):
    """Implementation of getting a wiki page by id."""
    result = wiki_client.get_page_by_id(
        project=project,
        wiki_identifier=wiki_id,
        id=id,
        recursion_level="oneLevel",
        include_content=True,
    )
    return _format_page(result.page)


def register_tools(mcp):
    """Register wiki tools with the MCP server."""

    @mcp.tool()
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

    @mcp.tool()
    def get_wiki_by_path(project: str, wiki_id: str, path: str):
        """Get Azure DevOps Wiki content by path returned from search_wiki.

        Use this tool when you need to:
        - Retrieve the full content of a wiki page when you know its path
        - Read a specific document from the wiki

        Args:
            project: The ID or name of the project
            wiki_id: The ID of the wiki
            path: The path to the wiki page

        Returns:
            The full content of the wiki page as a markdown string.
        """
        try:
            wiki_client = get_wiki_client()
            return _get_wiki_by_path_impl(wiki_client, project, wiki_id, path)
        except AzureDevOpsClientError as e:
            return f"Error: {str(e)}"

    @mcp.tool()
    def get_wiki_by_id(project: str, wiki_id: str, id: int):
        """Get Azure DevOps Wiki content by id returned from search_wiki.

        Use this tool when you need to:
        - Retrieve the full content of a wiki page when you know its ID
        - Read a specific document from the wiki using its unique identifier

        Args:
            project: The ID or name of the project
            wiki_id: The ID of the wiki
            id: The ID of the wiki page

        Returns:
            The full content of the wiki page as a markdown string.
        """
        try:
            wiki_client = get_wiki_client()
            return _get_wiki_by_id_impl(wiki_client, project, wiki_id, id)
        except AzureDevOpsClientError as e:
            return f"Error: {str(e)}"

"""
Tests for Azure DevOps Pipelines features.
"""

from unittest.mock import MagicMock, patch

from mcp_azure_devops.features.pipelines.tools.pipelines import (
    _format_pipeline,
    _get_pipeline_impl,
    _list_pipelines_impl,
)


def test_format_pipeline():
    """Test formatting a pipeline for display."""
    mock_pipeline = MagicMock()
    mock_pipeline.name = "Test Pipeline"
    mock_pipeline.id = 123
    mock_pipeline.folder = "/"
    mock_pipeline.revision = 1
    mock_pipeline._links = MagicMock()
    mock_pipeline._links.web.href = "http://example.com/pipeline"

    result = _format_pipeline(mock_pipeline)

    assert "## Test Pipeline" in result
    assert "- **ID**: 123" in result
    assert "- **Folder**: /" in result
    assert "- **Revision**: 1" in result
    assert "- **URL**: http://example.com/pipeline" in result


@patch("mcp_azure_devops.features.pipelines.common.get_connection")
def test_list_pipelines_impl(mock_get_connection):
    """Test listing pipelines."""
    mock_pipelines_client = MagicMock()
    mock_get_connection.return_value.clients.get_pipelines_client.return_value = mock_pipelines_client

    mock_pipeline1 = MagicMock()
    mock_pipeline1.name = "Pipeline 1"
    mock_pipeline1.id = 1
    mock_pipeline1.folder = "/"
    mock_pipeline1.revision = 1
    mock_pipeline1._links = MagicMock()
    mock_pipeline1._links.web.href = "http://pipeline1.com"

    mock_pipeline2 = MagicMock()
    mock_pipeline2.name = "Pipeline 2"
    mock_pipeline2.id = 2
    mock_pipeline2.folder = "/"
    mock_pipeline2.revision = 1
    mock_pipeline2._links = MagicMock()
    mock_pipeline2._links.web.href = "http://pipeline2.com"

    mock_pipelines_client.list_pipelines.return_value = [
        mock_pipeline1,
        mock_pipeline2,
    ]

    result = _list_pipelines_impl(mock_pipelines_client, "Test Project")

    assert "## Pipeline 1" in result
    assert "- **ID**: 1" in result
    assert "## Pipeline 2" in result
    assert "- **ID**: 2" in result


@patch("mcp_azure_devops.features.pipelines.common.get_connection")
def test_list_pipelines_impl_no_pipelines(mock_get_connection):
    """Test listing pipelines when none are found."""
    mock_pipelines_client = MagicMock()
    mock_get_connection.return_value.clients.get_pipelines_client.return_value = mock_pipelines_client
    mock_pipelines_client.list_pipelines.return_value = []

    result = _list_pipelines_impl(mock_pipelines_client, "Test Project")

    assert "No pipelines found in project Test Project." in result


@patch("mcp_azure_devops.features.pipelines.common.get_connection")
def test_get_pipeline_impl(mock_get_connection):
    """Test getting a pipeline."""
    mock_pipelines_client = MagicMock()
    mock_get_connection.return_value.clients.get_pipelines_client.return_value = mock_pipelines_client

    mock_pipeline = MagicMock()
    mock_pipeline.name = "Test Pipeline"
    mock_pipeline.id = 123
    mock_pipeline.folder = "/"
    mock_pipeline.revision = 1
    mock_pipeline._links = MagicMock()
    mock_pipeline._links.web.href = "http://example.com/pipeline"

    mock_pipelines_client.get_pipeline.return_value = mock_pipeline

    result = _get_pipeline_impl(mock_pipelines_client, "Test Project", 123)

    assert "## Test Pipeline" in result
    assert "- **ID**: 123" in result
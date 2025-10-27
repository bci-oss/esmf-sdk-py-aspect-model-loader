"""Data string resolver test suit."""
import pathlib

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.resolver.data_string import DataStringResolver


class TestDataStringResolver:
    """Data string resolver test suit."""

    @mock.patch("esmf_aspect_meta_model_python.resolver.data_string.AdaptiveGraph")
    @pytest.mark.parametrize("data_string", ["<samm:AspectModel>", pathlib.Path("data_string.ttl")])
    def test_read(self, rdf_graph_mock, data_string):
        graph_mock = mock.MagicMock(name="graph")
        rdf_graph_mock.return_value = graph_mock
        resolver = DataStringResolver()
        resolver.samm_version = "1.0.0"

        result = resolver.read(data_string)

        assert result == graph_mock
        graph_mock.parse.assert_called_once_with(data=str(data_string))
        rdf_graph_mock.assert_called_once_with(samm_version="1.0.0")

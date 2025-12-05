import pathlib

from unittest import mock

import pytest

from esmf_aspect_meta_model_python import utils


class TestParseGraphFromInput:
    @mock.patch("esmf_aspect_meta_model_python.utils.Graph", autospec=True)
    def test_from_path(self, graph_mock):
        input_source = pathlib.Path("input")

        result = utils._parse_graph_from_input(input_source)

        assert result is graph_mock.return_value
        graph_mock.return_value.parse.assert_called_once_with(input_source)

    @mock.patch("esmf_aspect_meta_model_python.utils.Graph", autospec=True)
    def test_from_data(self, graph_mock):
        input_source = "input data"

        result = utils._parse_graph_from_input(input_source)

        assert result is graph_mock.return_value
        graph_mock.return_value.parse.assert_called_once_with(data=input_source, format="turtle")


def test_get_samm_versions_from_graph():
    graph_mock = mock.MagicMock(name="graph")
    graph_mock.namespace_manager.namespaces.return_value = [
        ("samm", "urn:samm:org.eclipse.esmf.samm:meta-model:1.0.0#"),
        ("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
        ("samm-e", "urn:samm:org.eclipse.esmf.samm:entity:2.0.0#"),
        ("other", "http://example.com/other#"),
        ("samm1", "urn:samm:org.eclipse.esmf.samm:1.0.0#"),
        ("samm-c", "urn:samm:org.eclipse.esmf.samm:component:1.0.0#"),
        ("not-samm", "urn:not:samm:org.eclipse.esmf.samm:meta-model:3.0.0#"),
    ]

    result = list(utils.get_samm_versions_from_graph(graph_mock))

    assert result == ["1.0.0", "2.0.0", "1.0.0"]
    graph_mock.namespace_manager.namespaces.assert_called_once_with()


class TestHasVersionMismatchInGraph:
    @pytest.fixture
    def graph_mock(self):
        return mock.MagicMock(name="graph")

    def test_yes(self, graph_mock):
        graph_mock.namespace_manager.namespaces.return_value = [
            ("samm", "urn:samm:org.eclipse.esmf.samm:meta-model:1.0.0#"),
            ("samm-c", "urn:samm:org.eclipse.esmf.samm:meta-model:1.0.0#"),
            ("samm-e", "urn:samm:org.eclipse.esmf.samm:entity:2.0.0#"),
            ("samm2", "urn:samm:org.eclipse.esmf.samm:meta-model:1.0.0#"),
        ]

        result = utils.has_version_mismatch_in_graph(graph_mock, samm_version="1.0.0")

        assert result is True
        graph_mock.namespace_manager.namespaces.assert_called_once_with()

    def test_no(self, graph_mock):
        graph_mock.namespace_manager.namespaces.return_value = [
            ("samm", "urn:samm:org.eclipse.esmf.samm:meta-model:1.0.0#"),
            ("samm-e", "urn:samm:org.eclipse.esmf.samm:entity:1.0.0#"),
            ("samm-c", "urn:samm:org.eclipse.esmf.samm:entity:1.0.0#"),
        ]

        result = utils.has_version_mismatch_in_graph(graph_mock, samm_version="1.0.0")

        assert result is False
        graph_mock.namespace_manager.namespaces.assert_called_once_with()


@pytest.mark.parametrize("has_mismatch", [True, False])
@mock.patch("esmf_aspect_meta_model_python.utils._parse_graph_from_input", autospec=True)
@mock.patch("esmf_aspect_meta_model_python.utils.has_version_mismatch_in_graph", autospec=True)
def test_has_version_mismatch_from_input(mismatch_mock, parse_mock, has_mismatch):
    input_source = "input source"
    mismatch_mock.return_value = has_mismatch

    result = utils.has_version_mismatch_from_input(input_source, samm_version="1.0.0")

    assert result is has_mismatch
    parse_mock.assert_called_once_with(input_source)
    mismatch_mock.assert_called_once_with(parse_mock.return_value, samm_version="1.0.0")

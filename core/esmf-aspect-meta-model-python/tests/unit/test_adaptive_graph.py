#  Copyright (c) 2023 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0
import pathlib
import subprocess

from unittest import mock

import pytest

from rdflib import Graph

from esmf_aspect_meta_model_python.adaptive_graph import AdaptiveGraph
from esmf_aspect_meta_model_python.constants import SAMM_VERSION


@pytest.fixture
def graph():
    return AdaptiveGraph(samm_version="1.0.0")


class TestUpgradeTTLFile:
    def test_calls_samm_cli_prettyprint(self, graph):
        with mock.patch.object(graph._samm_cli, "prettyprint", return_value="content") as mock_prettyprint:
            result = graph._upgrade_ttl_file(pathlib.Path("file.ttl"))

        assert result == "content"
        mock_prettyprint.assert_called_once_with("file.ttl", capture=True)

    def test_raises_runtime_error_on_cli_failure(self, graph):
        err = subprocess.CalledProcessError(returncode=1, cmd="prettyprint", output="STDOUT", stderr="STDERR")

        with mock.patch.object(graph._samm_cli, "prettyprint", side_effect=err):
            with pytest.raises(RuntimeError, match="SAMM CLI failed for file.ttl:\nSTDOUT\nSTDERR"):
                graph._upgrade_ttl_file(pathlib.Path("file.ttl"))


@mock.patch.object(AdaptiveGraph, "_upgrade_ttl_file", return_value="upgraded content")
def test_upgrade_source(mock_cli, graph, tmp_path, capsys):
    file = tmp_path / "file.ttl"
    file.write_text("data")

    result = graph._upgrade_source(file)

    assert result == "upgraded content"
    assert isinstance(file, pathlib.Path)
    mock_cli.assert_called_once_with(file)

    captured = capsys.readouterr()
    assert f"SAMM version mismatch detected in {file}. Upgrading..." in captured.out


@pytest.mark.parametrize("input_data", ["string data", b"bytes data"])
@mock.patch.object(AdaptiveGraph, "_upgrade_ttl_file", return_value="upgraded content")
def test_upgrade_data(mock_cli, graph, capsys, input_data):
    result = graph._upgrade_data(input_data)

    assert result == "upgraded content"
    temp_file_path = pathlib.Path(mock_cli.call_args[0][0])
    mock_cli.assert_called_once_with(temp_file_path)
    assert not temp_file_path.exists()

    captured = capsys.readouterr()
    assert "[INFO] SAMM version mismatch detected in provided data" in captured.out


def test_set_samm_version(graph):
    graph.set_samm_version("2.0.0")

    assert graph._samm_version == "2.0.0"


class TestParse:
    @pytest.mark.parametrize(
        "source,data",
        [
            (None, None),  # Neither provided
            (pathlib.Path("file.ttl"), "data_content"),  # Both provided
        ],
    )
    def test_error_invalid_args(self, graph, source, data):
        with pytest.raises(ValueError, match="Either 'source' or 'data' must be provided."):
            graph.parse(source=source, data=data)

    def test_default_samm_version(self):
        assert AdaptiveGraph()._samm_version == SAMM_VERSION

    @pytest.mark.parametrize("source_type", [str, pathlib.Path])
    @mock.patch("esmf_aspect_meta_model_python.utils.has_version_mismatch_from_input", return_value=False)
    @mock.patch("rdflib.Graph.parse")
    def test_version_match(self, mock_parse, mock_version_check, graph, source_type):
        source = source_type("file.ttl")

        result = graph.parse(source=source)

        assert result is graph
        mock_version_check.assert_called_once_with(pathlib.Path("file.ttl"), samm_version="1.0.0")
        mock_parse.assert_called_once_with(source=pathlib.Path("file.ttl"), data=None)

    @mock.patch("esmf_aspect_meta_model_python.utils.has_version_mismatch_from_input", return_value=False)
    @mock.patch("rdflib.Graph.parse")
    def test_version_match_source_str(self, mock_parse, mock_version_check):
        graph = AdaptiveGraph(samm_version="1.0.0")
        source = "file.ttl"

        with mock.patch("pathlib.Path") as mock_path:
            result = graph.parse(source=source)

        assert result is graph
        mock_path.assert_called_once_with("file.ttl")
        mock_version_check.assert_called_once_with(mock_path.return_value, samm_version="1.0.0")
        mock_parse.assert_called_once_with(source=mock_path.return_value, data=None)

    @mock.patch("esmf_aspect_meta_model_python.utils.has_version_mismatch_from_input", return_value=True)
    @mock.patch.object(AdaptiveGraph, "_upgrade_source", return_value="upgraded ttl data")
    @mock.patch.object(AdaptiveGraph, "_upgrade_data")
    @mock.patch("rdflib.Graph.parse")
    def test_version_mismatch_from_file(
        self, mock_parse, mock_upgrade_data, mock_upgrade_source, mock_mismatch, graph, tmp_path
    ):
        fake_file = tmp_path / "data.ttl"
        fake_file.write_text("original ttl data")

        result = graph.parse(source=fake_file)

        assert result is graph
        mock_mismatch.assert_called_once_with(fake_file, samm_version="1.0.0")
        mock_upgrade_source.assert_called_once_with(fake_file)
        mock_upgrade_data.assert_not_called()
        mock_parse.assert_called_with(source=None, data="upgraded ttl data")

    @mock.patch("esmf_aspect_meta_model_python.utils.has_version_mismatch_from_input", return_value=True)
    @mock.patch.object(AdaptiveGraph, "_upgrade_source")
    @mock.patch.object(AdaptiveGraph, "_upgrade_data", return_value="upgraded ttl data")
    @mock.patch("rdflib.Graph.parse")
    def test_version_mismatch_from_data(
        self, mock_parse, mock_upgrade_data, mock_upgrade_source, mock_mismatch, graph, tmp_path
    ):
        result = graph.parse(data="original ttl data")

        assert result is graph
        mock_mismatch.assert_called_once_with("original ttl data", samm_version="1.0.0")
        mock_upgrade_data.assert_called_once_with("original ttl data")
        mock_upgrade_source.assert_not_called()
        mock_parse.assert_called_with(source=None, data="upgraded ttl data")

    @mock.patch.object(AdaptiveGraph, "_upgrade_ttl_file", side_effect=RuntimeError("CLI failed"))
    @mock.patch("esmf_aspect_meta_model_python.utils.has_version_mismatch_from_input", return_value=True)
    def test_error_upgrade_failure(self, mock_version_check, mock_upgrade, graph):
        with pytest.raises(RuntimeError, match="CLI failed"):
            graph.parse(data="some data")

        mock_version_check.assert_called_once_with("some data", samm_version="1.0.0")
        mock_upgrade.assert_called_once_with(mock.ANY)


@pytest.mark.parametrize(
    ("operation", "operation_name"),
    [
        ("add", "addition"),
        ("sub", "subtraction"),
        ("mul", "multiplication"),
    ],
)
class TestOperatorOverloads:
    def test_same_version(self, operation, operation_name, graph):
        g2 = AdaptiveGraph(samm_version="1.0.0")

        with mock.patch(f"rdflib.Graph.__{operation}__", return_value=g2):
            result = getattr(graph, f"__{operation}__")(g2)

        assert isinstance(result, AdaptiveGraph)
        assert result._samm_version == "1.0.0"

    def test_add_version_conflict(self, operation, operation_name, graph):
        g2 = AdaptiveGraph(samm_version="2.0.0")

        with mock.patch(f"rdflib.Graph.__{operation}__", return_value=g2):
            with pytest.raises(ValueError, match=f"SAMM version mismatch during {operation_name}."):
                getattr(graph, f"__{operation}__")(g2)

    def test_with_standard_graph(self, operation, operation_name, graph):
        g2 = Graph()

        with mock.patch(f"rdflib.Graph.__{operation}__", return_value=graph):
            result = getattr(graph, f"__{operation}__")(g2)

        assert isinstance(result, AdaptiveGraph)
        assert result._samm_version == "1.0.0"

    def test_result_not_adaptive_graph(self, operation, operation_name, graph):
        g2 = mock.MagicMock(spec=Graph)

        with mock.patch(f"rdflib.Graph.__{operation}__", return_value=g2):
            result = getattr(graph, f"__{operation}__")(g2)

        assert result is g2
        assert not hasattr(result, "_samm_version")

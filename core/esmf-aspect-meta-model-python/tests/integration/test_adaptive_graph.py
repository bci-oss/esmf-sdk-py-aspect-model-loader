from unittest import mock

import pytest

from esmf_aspect_meta_model_python.adaptive_graph import AdaptiveGraph


class TestAdaptiveGraphIntegration:
    @pytest.fixture
    def graph(self):
        return AdaptiveGraph(samm_version="1.0.0")

    def test_mismatch_from_file(self, graph, tmp_path, capsys):
        file_path = tmp_path / "bad_version.ttl"
        file_path.write_text(
            """
        @prefix samm: <urn:samm:org.eclipse.esmf.samm:aspect:9.9.9#> .
        samm:Aspect a samm:Aspect .
        """
        )
        upgraded_ttl = """
        @prefix samm: <urn:samm:org.eclipse.esmf.samm:aspect:1.0.0#> .
        samm:Aspect a samm:Aspect .
        """

        with mock.patch.object(graph._samm_cli, "prettyprint", return_value=upgraded_ttl) as mock_prettyprint:
            graph.parse(source=file_path, format="ttl")

        assert len(graph) == 1  # Ensure triple exists in graph
        ns_list = list(dict(graph.namespace_manager.namespaces()).values())
        assert any("1.0.0" in str(ns) for ns in ns_list)
        assert f"[INFO] SAMM version mismatch detected in {file_path}. Upgrading..." in capsys.readouterr().out
        mock_prettyprint.assert_called_once_with(str(file_path), capture=True)

    def test_mismatch_from_data(self, graph, capsys):
        bad_ttl_data = """
        @prefix samm: <urn:samm:org.eclipse.esmf.samm:aspect:2.0.0#> .
        samm:Aspect a samm:Aspect .
        """
        upgraded_ttl = """
        @prefix samm: <urn:samm:org.eclipse.esmf.samm:aspect:1.0.0#> .
        samm:Aspect a samm:Aspect .
        """

        with mock.patch.object(graph._samm_cli, "prettyprint", return_value=upgraded_ttl) as mock_prettyprint:
            graph.parse(data=bad_ttl_data, format="ttl")

        assert len(graph) == 1  # Assert the graph contains the upgraded triple
        ns_list = list(dict(graph.namespace_manager.namespaces()).values())
        assert any("1.0.0" in str(ns) for ns in ns_list)
        assert (
            "[INFO] SAMM version mismatch detected in provided data (target v1.0.0) Upgrading..."
            in capsys.readouterr().out
        )
        mock_prettyprint.assert_called_once_with(mock.ANY, capture=True)

    def test_integration_version_match_no_upgrade(self, graph, tmp_path, capsys):
        file_path = tmp_path / "good_version.ttl"
        file_path.write_text(
            """
        @prefix samm: <urn:samm:org.eclipse.esmf.samm:aspect:1.0.0#> .
        samm:Aspect a samm:Aspect .
        """
        )

        with mock.patch.object(graph._samm_cli, "prettyprint") as mock_cli:
            graph.parse(source=file_path, format="ttl")

        assert len(graph) == 1
        mock_cli.assert_not_called()
        assert capsys.readouterr().out == ""

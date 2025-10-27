import pathlib

from typing import Iterator, Union

from rdflib import Graph

from esmf_aspect_meta_model_python.constants import SAMM_NAMESPACE_PREFIX, SAMM_ORG_IDENTIFIER


def _parse_graph_from_input(input_source: Union[str, pathlib.Path]) -> Graph:
    """Create and populate an RDF graph from a path or Turtle string."""
    graph = Graph()

    if isinstance(input_source, pathlib.Path):
        graph.parse(input_source)
    else:  # str containing turtle data
        graph.parse(data=input_source, format="turtle")

    return graph


def get_samm_versions_from_graph(graph: Graph) -> Iterator[str]:
    """Yield all SAMM versions found in the RDF graph namespaces."""
    for prefix, namespace in graph.namespace_manager.namespaces():
        if prefix.startswith(SAMM_NAMESPACE_PREFIX):
            parts = namespace.split(":")

            if len(parts) >= 5 and parts[2] == SAMM_ORG_IDENTIFIER:
                yield parts[-1].strip("#")


def has_version_mismatch_in_graph(graph: Graph, samm_version: str) -> bool:
    """Check if there is a SAMM version mismatch in the provided RDF graph."""
    return any(v != samm_version for v in get_samm_versions_from_graph(graph))


def has_version_mismatch_from_input(input_source: Union[str, pathlib.Path], samm_version: str) -> bool:
    """Detect SAMM version mismatch from an input source (path or Turtle string)."""
    return has_version_mismatch_in_graph(_parse_graph_from_input(input_source), samm_version=samm_version)


def get_samm_version_from_input(input_source: Union[str, pathlib.Path]) -> str:
    """Retrieve the SAMM version from the provided input source (path or Turtle string)."""
    version = ""

    for v in get_samm_versions_from_graph(_parse_graph_from_input(input_source)):
        version = v

    return version

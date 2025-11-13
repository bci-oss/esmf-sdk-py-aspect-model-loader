"""Base resolver test suit."""
from unittest import mock

import pytest

from rdflib import Graph

from esmf_aspect_meta_model_python.resolver.base import ResolverInterface


class ResolverTest(ResolverInterface):
    """Resolver interface test class."""

    def read(self, input_data):
        return Graph()

    def get_aspect_urn(self):
        return "aspect_urn"


class TestResolverInterface:
    """Resolver interface test suit."""

    def test_validate_samm_version_no_version(self):
        with pytest.raises(ValueError) as error:
            ResolverInterface._validate_samm_version("")

        assert str(error.value) == "SAMM version not found in the Graph."

    @mock.patch("esmf_aspect_meta_model_python.resolver.base.SammUnitsGraph")
    def test_validate_samm_version_not_supported_version(self, samm_units_graph_mock):
        samm_units_graph_mock.SAMM_VERSION = "2"
        with pytest.raises(ValueError) as error:
            ResolverInterface._validate_samm_version("3")

        assert str(error.value) == "3 is not supported SAMM version."

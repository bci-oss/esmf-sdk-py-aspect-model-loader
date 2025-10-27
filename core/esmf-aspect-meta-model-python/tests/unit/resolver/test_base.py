"""Base resolver test suit."""
import pathlib

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

    @mock.patch("esmf_aspect_meta_model_python.resolver.base.ResolverInterface._validate_samm_version")
    @mock.patch("esmf_aspect_meta_model_python.utils.get_samm_version_from_input")
    @pytest.mark.parametrize("stream_input", ["stream1", pathlib.Path("file_path")])
    def test_set_samm_version(self, get_samm_version_from_input_mock, validate_samm_version_mock, stream_input):
        get_samm_version_from_input_mock.return_value = version = "1.2.3"
        resolver = ResolverTest()

        resolver.set_samm_version(stream_input)

        get_samm_version_from_input_mock.assert_called_once_with(stream_input)
        validate_samm_version_mock.assert_called_once_with(get_samm_version_from_input_mock.return_value)
        assert resolver.samm_version == version

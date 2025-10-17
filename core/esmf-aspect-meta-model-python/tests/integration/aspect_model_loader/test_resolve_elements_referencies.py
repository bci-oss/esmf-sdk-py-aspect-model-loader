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

from pathlib import Path

import pytest

from esmf_aspect_meta_model_python import SAMMGraph

ASPECT_MODELS_DIR = (
    Path.cwd() / "tests/integration/aspect_model_loader/resources/org.eclipse.esmf.test.general_with_references"
)

ASPECT_MODELS_V2_1_0 = ASPECT_MODELS_DIR / "2.1.0"
ASPECT_MODELS_V2_2_0 = ASPECT_MODELS_DIR / "2.2.0"


def test_resolve_elements_references():
    file_path = ASPECT_MODELS_V2_1_0 / "AspectWithReferences.ttl"
    samm_graph = SAMMGraph()
    samm_graph.parse(file_path)
    aspect = samm_graph.load_aspect_model()

    assert aspect.name == "test_aspect"
    assert aspect.get_preferred_name("en") == "Aspect with references"
    assert aspect.get_description("en") == "Test aspect with references from different files."

    property_1 = aspect.properties[0]
    assert property_1.name == "property_1"
    assert property_1.get_preferred_name("en") == "Test property"
    assert property_1.get_description("en") == "Test property description."

    property_2 = property_1.properties[0]
    assert property_2.name == "ExternalPartId"
    assert property_2.get_preferred_name("en") == "External part id"
    assert property_2.get_description("en") == "External part id description."
    assert str(property_2.example_value) == "0123456789"

    property_3 = property_2.characteristic
    assert property_3.name == "PartNumber"
    assert property_3.see == ["https://some_link"]
    assert property_3.base_characteristic.get_preferred_name("en") == "Part Number"
    assert property_3.constraints[0].value == "[A-Z0-9-]{10,68}"

    property_4 = property_1.properties[1]
    assert property_4.name == "TypeList"
    assert property_4.get_preferred_name("en") == "Test List"
    assert property_4.get_description("en") == "This is a test list."
    assert property_4.see == ["http://example.com/"]


def test_aspect_with_diff_meta_model_submodel_version():
    file_path = ASPECT_MODELS_V2_2_0 / "AspectWithEarlierSubmodelVersionReferences.ttl"
    samm_graph = SAMMGraph()
    samm_graph.parse(file_path)

    with pytest.raises(
        ValueError,
        match=(
            "SAMM version mismatch. Found '2.1.0', but expected '2.2.0'. "
            "Ensure all RDF files use a single, consistent SAMM version"
        ),
    ):
        samm_graph.load_aspect_model()

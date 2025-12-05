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

from esmf_aspect_meta_model_python import SAMMGraph

ASPECT_MODELS_DIR = (
    Path.cwd() / "tests/integration/aspect_model_loader/resources/org.eclipse.esmf.test.general_with_invalid_versions"
)

ASPECT_MODELS_V2_2_0 = ASPECT_MODELS_DIR / "2.2.0"


def test_upgrade_files(capsys):
    file_path = ASPECT_MODELS_V2_2_0 / "AspectWithReferences.ttl"
    samm_graph = SAMMGraph()
    samm_graph.parse(file_path)

    aspect = samm_graph.load_aspect_model()

    # Asserts
    out_lines = [line for line in capsys.readouterr().out.splitlines() if line.strip()]
    paths = [
        ASPECT_MODELS_DIR.parent / "org.eclipse.esmf.test.types/2.1.0/type_shared.ttl",
        ASPECT_MODELS_DIR.parent / "org.eclipse.esmf.test.general_with_invalid_versions/2.2.0/Part_shared.ttl",
    ]
    expected_lines = [
        f"[INFO] SAMM version mismatch detected in {paths[0]}. Upgrading...",
        f"[INFO] SAMM version mismatch detected in {paths[1]}. Upgrading...",
    ]
    assert len(out_lines) == len(expected_lines)
    assert set(out_lines) == set(expected_lines)

    assert aspect.name == "AspectWithReferences"
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


def test_upgrade_data(capsys):
    data = """
        #
        # Copyright (c) 2023 Robert Bosch Manufacturing Solutions GmbH, Germany. All rights reserved.
        #
        
        @prefix : <urn:samm:org.eclipse.esmf.test.general_with_references:2.2.0#> .
        @prefix samm: <urn:samm:org.eclipse.esmf.samm:meta-model:2.2.0#> .
        @prefix samm-c: <urn:samm:org.eclipse.esmf.samm:characteristic:2.2.0#> .
        @prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
        
        :testProperty a samm:Property ;
           samm:characteristic :TestEnumeration ;
           samm:preferredName "Test Enumeration"@en ;
           samm:description "This is a test for enumeration."@en ;
           samm:exampleValue "unit:hectopascal"^^samm:curie . 
        
        :TestEnumeration a samm-c:Enumeration ;
           samm:preferredName "Test Enumeration"@en ;
           samm:description "This is a test for enumeration."@en ;
           samm:dataType samm:curie ;
           samm-c:values ( "unit:hectopascal"^^samm:curie "unit:gram"^^samm:curie ) .
           
        #
        # Copyright (c) 2023 Robert Bosch Manufacturing Solutions GmbH, Germany. All rights reserved.
        #
        
        @prefix : <urn:samm:org.eclipse.esmf.test.general_with_references:2.2.0#> .
        @prefix samm: <urn:samm:org.eclipse.esmf.samm:meta-model:2.1.0#> .
        @prefix samm-c: <urn:samm:org.eclipse.esmf.samm:characteristic:2.2.0#> .
        @prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
        
        :AspectWithEarlierSubmodelVersionReferences a samm:Aspect ;
            samm:preferredName "Aspect with references"@en ;
            samm:description "Test aspect with references from different files."@en ;
            samm:properties ( :testProperty ) ;
            samm:operations ( ) .
    """  # noqa W293 W291 trailing whitespace

    samm_graph = SAMMGraph()
    samm_graph.parse(data)

    aspect = samm_graph.load_aspect_model()

    # Asserts
    assert (
        capsys.readouterr().out
        == "[INFO] SAMM version mismatch detected in provided data (target v2.2.0) Upgrading...\n"
    )
    assert aspect.name == "AspectWithEarlierSubmodelVersionReferences"
    assert aspect.get_preferred_name("en") == "Aspect with references"
    assert aspect.get_description("en") == "Test aspect with references from different files."

    property_1 = aspect.properties[0]
    assert property_1.name == "testProperty"
    assert property_1.get_preferred_name("en") == "Test Enumeration"
    assert property_1.get_description("en") == "This is a test for enumeration."
    assert property_1.data_type.urn == "urn:samm:org.eclipse.esmf.samm:meta-model:2.2.0#curie"
    assert str(property_1.example_value) == "unit:hectopascal"

    characteristic = property_1.characteristic
    assert characteristic.data_type.urn == "urn:samm:org.eclipse.esmf.samm:meta-model:2.2.0#curie"
    assert characteristic.get_preferred_name("en") == "Test Enumeration"
    assert characteristic.get_description("en") == "This is a test for enumeration."
    assert [str(value) for value in characteristic.values] == ["unit:hectopascal", "unit:gram"]

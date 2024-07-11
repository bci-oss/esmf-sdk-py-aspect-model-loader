"""Example for the Aspect model with entity.

model: pydentic\examples\models\samm_2_1_0\org.eclipse.esmf.test\1.0.0\AAspectWithEntity.ttl
"""

from esmf_aspect_meta_model_python.pydentic.meta_model_elements.aspect import Aspect
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.property import Property
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.scalar import Scalar
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.single_entity import SingleEntity
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.entity import Entity


entity_property = Characteristic(
    name="Text",
    preferred_names={'en': 'Text'},
    descriptions={
        'en': (
            'Describes a Property which contains plain text. This is intended exclusively for human readable strings, '
            'not for identifiers, measurement values, etc.'
        )
    },
    meta_model_version="2.1.0",
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#string",
    ),
    urn="urn:samm:org.eclipse.esmf.samm:characteristic:2.1.0#Text",
)

entity_property = Property(
    name="entityProperty",
    preferred_names={'en': 'Entity Property'},
    descriptions={'en': 'This is a property for the test entity.'},
    meta_model_version="2.1.0",
    characteristic=[entity_property],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#entityProperty",
)
entity_property.append_parent_element(entity_property)

data_type_entity = Entity(
    name="DataTypeEntity",
    preferred_names={'en': 'Test Entity'},
    descriptions={'en': 'This is a test entity'},
    meta_model_version="2.1.0",
    properties=[entity_property],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#DataTypeEntity",
)
entity_property.append_parent_element(data_type_entity)

single_entity_characteristic = SingleEntity(
    name="SingleEntityCharacteristic",
    preferred_names={'en': 'Test Entity Characteristic'},
    descriptions={'en': 'This is a test Entity Characteristic'},
    meta_model_version="2.1.0",
    see=['http://example.com/'],
    data_type=data_type_entity,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#SingleEntityCharacteristic",
)
data_type_entity.append_parent_element(single_entity_characteristic)

single_entity_property = Property(
    name="singleEntityProperty",
    preferred_names={'en': 'Test Property'},
    descriptions={'en': 'This is a test property.'},
    meta_model_version="2.1.0",
    see=['http://example.com/', 'http://example.com/me'],
    characteristic=single_entity_characteristic,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#singleEntityProperty",
)
single_entity_characteristic.append_parent_element(single_entity_property)

aspect = Aspect(
    name="AspectWithEntity",
    preferred_names={'en': 'Test Aspect'},
    descriptions={'en': 'This is a test description'},
    meta_model_version="2.1.0",
    see=['http://example.com/'],
    properties=[single_entity_property],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#AspectWithEntity",
)
single_entity_property.append_parent_element(aspect)

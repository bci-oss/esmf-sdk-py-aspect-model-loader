"""Example for the Aspect model with enumeration.

model: pydentic\examples\models\samm_2_1_0\org.eclipse.esmf.test\1.0.0\AspectWithEnumeration.ttl
"""

from esmf_aspect_meta_model_python.pydentic.meta_model_elements.aspect import Aspect
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.property import Property
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.scalar import Scalar
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.enumeration import Enumeration


enumeration_characteristic = Enumeration(
    name="enumerationCharacteristic",
    preferred_names={'en': 'Test Enumeration'},
    descriptions={'en': 'This is a test for enumeration.'},
    meta_model_version="2.1.0",
    see=['http://example.com/'],
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#integer",
    ),
    values=[1, 2, 3],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#enumerationCharacteristic",
)

enumeration_property = Property(
    name="enumerationProperty",
    preferred_names={'en': 'Test Property'},
    descriptions={'en': 'This is a test property.'},
    meta_model_version="2.1.0",
    see=['http://example.com/', 'http://example.com/me'],
    characteristic=enumeration_characteristic,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#enumerationProperty",
)
enumeration_characteristic.append_parent_element(enumeration_property)

aspect = Aspect(
    name="AspectWithEnumeration",
    preferred_names={'en': 'Test Aspect'},
    descriptions={'en': 'This is a test description'},
    meta_model_version="2.1.0",
    see=['http://example.com/'],
    properties=[enumeration_property],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#AspectWithEnumeration",
)
enumeration_property.append_parent_element(aspect)

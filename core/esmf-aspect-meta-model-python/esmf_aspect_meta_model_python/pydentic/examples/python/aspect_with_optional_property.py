"""Example for the Aspect model with optional property.

model: pydentic\examples\models\samm_2_1_0\org.eclipse.esmf.test\1.0.0\AspectWithOptionalProperty.ttl
"""

from esmf_aspect_meta_model_python.pydentic.meta_model_elements.aspect import Aspect
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.property import Property
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.scalar import Scalar


text_characteristic = Characteristic(
    # node from the SAMM specification samm\characteristic\2.1.0\characteristic-instances.ttl samm-c:Text
    name="Text",
    preferred_names={"en": "Text"},
    descriptions={
        "en": (
            "Describes a Property which contains plain text. This is intended exclusively for human readable "
            "strings, not for identifiers, measurement values, etc."
        ),
    },
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#string",
    )
)

optional_property = Property(
    name="testProperty",
    preferred_names={"en": "Test Property"},
    descriptions={"en": "This is a test property."},
    meta_model_version="2.1.0",
    see=["<http://example.com/>", "<http://example.com/me>"],
    characteristic=text_characteristic,
    is_optional=True,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#testProperty",
)
text_characteristic.append_parent_element(optional_property)

aspect = Aspect(
    name="AspectWithOptionalProperty",
    preferred_names={"en": "Test Aspect"},
    descriptions={"en": "This is a test description"},
    meta_model_version="2.1.0",
    see=["<http://example.com/>"],
    properties=[optional_property],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#AspectWithOptionalProperty",
)
optional_property.append_parent_element(aspect)

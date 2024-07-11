"""Example for the Aspect model with optional properties.

model: pydentic\examples\models\samm_2_1_0\org.eclipse.esmf.test\1.0.0\AspectWithOptionalProperties.ttl
"""

from esmf_aspect_meta_model_python.pydentic.meta_model_elements.aspect import Aspect
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.property import Property
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.quantifiable.quantifiable import (
    Quantifiable,
)
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.unit import Unit
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.data_type import DataType
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.scalar import Scalar


timestamp_characteristic = Characteristic(
    name="Timestamp",
    preferred_names={'en': 'Timestamp'},
    descriptions={'en': 'Describes a Property which contains the date and time with an optional timezone.'},
    meta_model_version="2.1.0",
    data_type=Scalar(
        urn="http://www.w3.org/2001/XMLSchema#dateTime",
        meta_model_version="2.1.0",
    ),
)

timestamp_property = Property(
    name="timestampProperty",
    meta_model_version="2.1.0",
    characteristic=timestamp_characteristic,
    is_optional=True,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#timestampProperty",
)
timestamp_characteristic.append_parent_element(timestamp_characteristic)

quantity_kind_units = {
    Unit(
        name="displacementVectorOfIonOrAtom",
        preferred_names={"en": "displacement vector of ion or atom"},
        meta_model_version="2.1.0",
        urn="urn:samm:org.eclipse.esmf.samm:unit:2.1.0#displacementVectorOfIonOrAtom",
    ),
    Unit(
        name="breadth",
        preferred_names={'en': 'breadth'},
        meta_model_version="2.1.0",
        urn="urn:samm:org.eclipse.esmf.samm:unit:2.1.0#breadth",
    ),
    # There are more quantity kind subunits
    # see "unit:metre" at samm\unit\2.1.0\units.ttl
}

metre_unit = Unit(
    name="metre",
    preferred_names={'en': 'metre'},
    meta_model_version="2.1.0",
    symbol="m",
    code="MTR",
    quantity_kinds=quantity_kind_units,
    urn="urn:samm:org.eclipse.esmf.samm:unit:2.1.0#metre"
)
for sub_unit in quantity_kind_units:
    sub_unit.append_parent_element(metre_unit)

quantifiable_characteristic = Quantifiable(
    name="numberProperty_characteristic",
    meta_model_version="2.1.0",
    data_type=DataType(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#unsignedLong",
    ),
    unit=metre_unit,
)
metre_unit.append_parent_element(quantifiable_characteristic)

number_property = Property(
    name="numberProperty",
    meta_model_version="2.1.0",
    characteristic=quantifiable_characteristic,
    is_optional=True,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#numberProperty",
)
quantifiable_characteristic.append_parent_element(number_property)

aspect = Aspect(
    name="AspectWithOptionalProperties",
    meta_model_version="2.1.0",
    properties=[number_property, timestamp_property],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#AspectWithOptionalProperties",
)
number_property.append_parent_element(aspect)
timestamp_property.append_parent_element(aspect)

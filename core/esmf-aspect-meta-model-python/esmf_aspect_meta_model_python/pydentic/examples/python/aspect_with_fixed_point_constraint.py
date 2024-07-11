"""Example for the Aspect model with fixed point constraint.

model: pydentic\examples\models\samm_2_1_0\org.eclipse.esmf.test\1.0.0\AAspectWithFixedPointConstraint.ttl
"""

from esmf_aspect_meta_model_python.pydentic.meta_model_elements.aspect import Aspect
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.property import Property
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.unit import Unit
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.data_type import DataType
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.scalar import Scalar
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.trait import Trait
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.constraints.fixed_point_constraint import (
    FixedPointConstraint,
)
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.quantifiable.measurement import (
    Measurement,
)


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
        name="instantaneousSoundParticleVelocity",
        preferred_names={'en': '(instantaneous) sound particle velocity'},
        meta_model_version="2.1.0",
        urn="urn:samm:org.eclipse.esmf.samm:unit:2.1.0#instantaneousSoundParticleVelocity",
    ),
    Unit(
        name="groupVelocity",
        preferred_names={'en': 'group velocity'},
        meta_model_version="2.1.0",
        urn="urn:samm:org.eclipse.esmf.samm:unit:2.1.0#groupVelocity",
    ),
    # There are more quantity kind subunits
    # see "unit:metrePerSecond" at samm\unit\2.1.0\units.ttl
}

metre_per_second_unit = Unit(
    name="metrePerSecond",
    preferred_names={'en': 'metre per second'},
    meta_model_version="2.1.0",
    symbol="m/s",
    code="MTS",
    quantity_kinds=quantity_kind_units,
    urn="urn:samm:org.eclipse.esmf.samm:unit:2.1.0#metrePerSecond"
)
for sub_unit in quantity_kind_units:
    sub_unit.append_parent_element(metre_per_second_unit)

fixed_point_constraint_base_characteristic = Measurement(
    name="metrePerSecondMeasurement",
    meta_model_version="2.1.0",
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#float",
    ),
    unit=metre_per_second_unit,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#metrePerSecondMeasurement",
)
metre_per_second_unit.append_parent_element(fixed_point_constraint_base_characteristic)

fixed_point_constraint = FixedPointConstraint(
    name="fixedPointConstraint_constraint",
    preferred_names={'en': 'Test Fixed Point'},
    descriptions={'en': 'This is a test fixed point constraint.'},
    meta_model_version="2.1.0",
    see=['http://example.com/'],
    scale=5,
    integer=3,
)

fixed_point_constraint_characteristic = Trait(
    name="fixedPointConstraint",
    meta_model_version="2.1.0",
    data_type=DataType(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#float",
    ),
    base_characteristic=fixed_point_constraint_base_characteristic,
    constraints=[fixed_point_constraint],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#fixedPointConstraint",
)
fixed_point_constraint_base_characteristic.append_parent_element(fixed_point_constraint_characteristic)
fixed_point_constraint.append_parent_element(fixed_point_constraint_characteristic)

fixed_point_constraint_property = Property(
    name="fixedPointConstraintProperty",
    meta_model_version="2.1.0",
    characteristic=fixed_point_constraint_characteristic,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#fixedPointConstraintProperty",
)
fixed_point_constraint_characteristic.append_parent_element(fixed_point_constraint_property)

aspect = Aspect(
    name="AspectWithFixedPointConstraint",
    preferred_names={'en': 'Test Aspect'},
    descriptions={'en': 'This is a test description'},
    meta_model_version="2.1.0",
    see=['http://example.com/'],
    properties=[fixed_point_constraint_property],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#AspectWithFixedPointConstraint",
)
fixed_point_constraint_property.append_parent_element(aspect)

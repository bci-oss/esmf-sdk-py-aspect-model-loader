"""Example for the Aspect model with constraints.

model: pydentic\examples\models\samm_2_1_0\org.eclipse.esmf.test\1.0.0\AspectWithConstraint.ttl
"""

from esmf_aspect_meta_model_python.pydentic.meta_model_elements.aspect import Aspect
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.property import Property
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.unit import Unit
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.scalar import Scalar
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.trait import Trait
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.constraints.length_constraint import LengthConstraint
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.constraints.range_constraint import RangeConstraint
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.constraints.regular_expression_constraint import (
    RegularExpressionConstraint,
)
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.bound_definition import BoundDefinition
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.quantifiable.measurement import Measurement


# ---------------- LengthConstraint ----------------
length_constraint = LengthConstraint(
    name="StringLengthConstraint_constraint",
    meta_model_version="2.1.0",
    min_value=20,
    max_value=22,
)

string_length_constraint_base_characteristic = Characteristic(
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

string_length_constraint_characteristic = Trait(
    name="StringLengthConstraint",
    preferred_names={'en': 'Used Test Constraint'},
    descriptions={'en': 'Used Test Constraint'},
    meta_model_version="2.1.0",
    see=['http://example.com/', 'http://example.com/me'],
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#string",
    ),
    base_characteristic=string_length_constraint_base_characteristic,
    constraints=[length_constraint],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#StringLengthConstraint",
)
string_length_constraint_base_characteristic.append_parent_element(string_length_constraint_characteristic)
length_constraint.append_parent_element(string_length_constraint_characteristic)

string_length_constraint_property = Property(
    name="stringLcProperty",
    meta_model_version="2.1.0",
    characteristic=string_length_constraint_characteristic,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#stringLcProperty",
)
string_length_constraint_characteristic.append_parent_element(string_length_constraint_property)

# ---------------- DoubleRangeConstraint ----------------

quantity_kinds_units = {
    Unit(
        name="accelerationOfFreeFall",
        preferred_names={'en': 'acceleration of free fall'},
        meta_model_version="2.1.0",
        urn="urn:samm:org.eclipse.esmf.samm:unit:2.1.0#accelerationOfFreeFall",
    ),
    Unit(
        name="instantaneousSoundParticleAcceleration",
        preferred_names={'en': '(instantaneous) sound particle acceleration'},
        meta_model_version="2.1.0",
        urn="urn:samm:org.eclipse.esmf.samm:unit:2.1.0#instantaneousSoundParticleAcceleration",
    ),
    Unit(
        name="accelerationDueToGravity",
        preferred_names={'en': 'acceleration due to gravity'},
        meta_model_version="2.1.0",
        urn="urn:samm:org.eclipse.esmf.samm:unit:2.1.0#accelerationDueToGravity",
    ),
    Unit(
        name="acceleration",
        preferred_names={'en': 'acceleration'},
        meta_model_version="2.1.0",
        urn="urn:samm:org.eclipse.esmf.samm:unit:2.1.0#acceleration",
    ),
}

metre_per_second_squared_unit = Unit(
    name="metrePerSecondSquared",
    preferred_names={'en': 'metre per second squared'},
    meta_model_version="2.1.0",
    symbol="m/s²",
    code="MSK",
    quantity_kinds=quantity_kinds_units,
    unrn="urn:samm:org.eclipse.esmf.samm:unit:2.1.0#metrePerSecondSquared",
)
for sub_unit in quantity_kinds_units:
    sub_unit.append_parent_element(metre_per_second_squared_unit)

double_range_constraint_base_characteristic = Measurement(
    name="DoubleMeasurement",
    descriptions={'en': 'The acceleration'},
    meta_model_version="2.1.0",
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#double",
    ),
    unit=metre_per_second_squared_unit,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#DoubleMeasurement",
)
metre_per_second_squared_unit.append_parent_element(double_range_constraint_base_characteristic)

range_constraint = RangeConstraint(
    name="DoubleRangeConstraint_constraint",
    meta_model_version="2.1.0",
    lower_bound_definition=BoundDefinition.AT_LEAST,
    upper_bound_definition=BoundDefinition.AT_MOST,
)

double_range_constraint_characteristic = Trait(
    name="DoubleRangeConstraint",
    preferred_names={'en': 'Test Constraint'},
    descriptions={'en': 'Test Constraint'},
    meta_model_version="2.1.0",
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#double",
    ),
    base_characteristic=double_range_constraint_base_characteristic,
    constraints=[range_constraint],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#DoubleRangeConstraint",
)
double_range_constraint_base_characteristic.append_parent_element(double_range_constraint_characteristic)
range_constraint.append_parent_element(double_range_constraint_characteristic)

double_range_constraint_property = Property(
    name="doubleRcProperty",
    meta_model_version="2.1.0",
    characteristic=double_range_constraint_characteristic,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#doubleRcProperty",
)
double_range_constraint_characteristic.append_parent_element(double_range_constraint_property)

# ---------------- IntegerRangeConstraint ----------------

integer_range_constraint_base_characteristic = Measurement(
    name="IntegerMeasurement",
    descriptions={'en': 'The acceleration'},
    meta_model_version="2.1.0",
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#int",
    ),
    unit=metre_per_second_squared_unit,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#IntegerMeasurement",
)

integer_range_constraint = RangeConstraint(
    name="IntegerRangeConstraint_constraint",
    meta_model_version="2.1.0",
    min_value=-1,
    max_value=-1,
    lower_bound_definition=BoundDefinition.AT_LEAST,
    upper_bound_definition=BoundDefinition.AT_MOST,
)

integer_range_constraint_characteristic = Trait(
    name="IntegerRangeConstraint",
    preferred_names={'en': 'Test Constraint'},
    descriptions={'en': 'Test Constraint'},
    meta_model_version="2.1.0",
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#int",
    ),
    base_characteristic=integer_range_constraint_base_characteristic,
    constraints=[integer_range_constraint],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#IntegerRangeConstraint",
)
integer_range_constraint_base_characteristic.append_parent_element(integer_range_constraint_characteristic)
integer_range_constraint.append_parent_element(integer_range_constraint_characteristic)

integer_range_constraint_property = Property(
    name="intRcProperty",
    meta_model_version="2.1.0",
    characteristic=integer_range_constraint_characteristic,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#intRcProperty",
)
integer_range_constraint_characteristic.append_parent_element(integer_range_constraint_property)

# ---------------- BigIntegerRangeConstraint ----------------

big_integer_range_constraint_base_characteristic = Measurement(
    name="BigIntegerMeasurement",
    descriptions={'en': 'The acceleration'},
    meta_model_version="2.1.0",
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#integer",
    ),
    unit=metre_per_second_squared_unit,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#BigIntegerMeasurement",
)

big_integer_range_constraint = RangeConstraint(
    name="BigIntegerRangeConstraint_constraint",
    meta_model_version="2.1.0",
    min_value=10,
    max_value=15,
    lower_bound_definition=BoundDefinition.AT_LEAST,
    upper_bound_definition=BoundDefinition.AT_MOST,
)

big_integer_range_constraint_characteristic = Trait(
    name="BigIntegerRangeConstraint",
    preferred_names={'en': 'Test Constraint'},
    descriptions={'en': 'Test Constraint'},
    meta_model_version="2.1.0",
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#integer",
    ),
    base_characteristic=big_integer_range_constraint_base_characteristic,
    constraints=[big_integer_range_constraint],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#BigIntegerRangeConstraint",
)
big_integer_range_constraint_base_characteristic.append_parent_element(big_integer_range_constraint_characteristic)
big_integer_range_constraint.append_parent_element(big_integer_range_constraint_characteristic)

big_integer_range_constraint_property = Property(
    name="bigIntRcProperty",
    meta_model_version="2.1.0",
    characteristic=big_integer_range_constraint_characteristic,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#bigIntRcProperty",
)
big_integer_range_constraint_characteristic.append_parent_element(big_integer_range_constraint_property)

# ---------------- FloatRangeConstraint ----------------

float_range_constraint_base_characteristic = Measurement(
    name="FloatMeasurement",
    descriptions={'en': 'The acceleration'},
    meta_model_version="2.1.0",
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#float",
    ),
    unit=metre_per_second_squared_unit,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#FloatMeasurement",
)

float_range_constraint = RangeConstraint(
    name="FloatRangeConstraint_constraint",
    meta_model_version="2.1.0",
    min_value=100.0,
    max_value=112.0,
    lower_bound_definition=BoundDefinition.AT_LEAST,
    upper_bound_definition=BoundDefinition.AT_MOST,
)

float_range_constraint_characteristic = Trait(
    name="FloatRangeConstraint",
    preferred_names={'en': 'Test Constraint'},
    descriptions={'en': 'Test Constraint'},
    meta_model_version="2.1.0",
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#float",
    ),
    base_characteristic=float_range_constraint_base_characteristic,
    constraints=[float_range_constraint],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#FloatRangeConstraint",
)
float_range_constraint_base_characteristic.append_parent_element(float_range_constraint_characteristic)
float_range_constraint.append_parent_element(float_range_constraint_characteristic)

float_range_constraint_property = Property(
    name="floatRcProperty",
    meta_model_version="2.1.0",
    characteristic=float_range_constraint_characteristic,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#floatRcProperty",
)
float_range_constraint_characteristic.append_parent_element(float_range_constraint_property)

# ---------------- stringRegexConstraint ----------------

string_regular_expression_constraint_base_characteristic = Characteristic(
    name="RegularExpressionConstraint",
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

string_regular_expression_constraint = RegularExpressionConstraint(
    name="RegularExpressionConstraint_constraint",
    meta_model_version="2.1.0",
    value="[a-zA-Z]",
)

string_regular_expression_constraint_characteristic = Characteristic(
    name="RegularExpressionConstraint",
    preferred_names={'en': 'Test Regular Expression Constraint'},
    descriptions={'en': 'Test Regular Expression Constraint'},
    meta_model_version="2.1.0",
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#string",
    ),
    base_characteristic=string_regular_expression_constraint_base_characteristic,
    constraints=[string_regular_expression_constraint],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#RegularExpressionConstraint",
)
string_regular_expression_constraint_base_characteristic.append_parent_element(
    string_regular_expression_constraint_characteristic
)
string_regular_expression_constraint.append_parent_element(string_regular_expression_constraint_characteristic)

string_regular_expression_constraint_property = Property(
    name="stringRegexcProperty",
    meta_model_version="2.1.0",
    characteristic=string_regular_expression_constraint_characteristic,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#stringRegexcProperty",
)
string_regular_expression_constraint_characteristic.append_parent_element(string_regular_expression_constraint_property)


aspect = Aspect(
    name="AspectWithConstraint",
    meta_model_version="2.1.0",
    properties=[
        string_length_constraint_property,
        double_range_constraint_property,
        integer_range_constraint_property,
        big_integer_range_constraint_property,
        float_range_constraint_property,
        string_regular_expression_constraint_property,
    ],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#AspectWithConstraint",
)
string_length_constraint_property.append_parent_element(aspect)
double_range_constraint_property.append_parent_element(aspect)
integer_range_constraint_property.append_parent_element(aspect)
big_integer_range_constraint_property.append_parent_element(aspect)
float_range_constraint_property.append_parent_element(aspect)
string_regular_expression_constraint_property.append_parent_element(aspect)

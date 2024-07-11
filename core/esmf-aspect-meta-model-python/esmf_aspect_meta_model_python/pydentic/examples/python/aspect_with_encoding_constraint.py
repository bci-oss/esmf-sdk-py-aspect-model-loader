"""Example for the Aspect model with encoding constraints.

model: pydentic\examples\models\samm_2_1_0\org.eclipse.esmf.test\1.0.0\AspectWithEncodingConstraint.ttl
"""

from rdflib.term import Literal

from esmf_aspect_meta_model_python.pydentic.meta_model_elements.aspect import Aspect
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.property import Property
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.scalar import Scalar
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.trait import Trait
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.constraints.encoding_constraint import EncodingConstraint


encoding_constraint_base_characteristic = Characteristic(
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

encoding_constraint = EncodingConstraint(
    name="TestEncodingConstraint_constraint",
    preferred_names={'en': 'Test Encoding Constraint'},
    descriptions={'en': 'This is a test encoding constraint.'},
    meta_model_version="2.1.0",
    see=['http://example.com/'],
    value="UTF-8",
)

encoding_constraint_characteristic = Trait(
    name="EncodingConstraint",
    meta_model_version="2.1.0",
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#string",
    ),
    base_characteristic=encoding_constraint_base_characteristic,
    constraints=[encoding_constraint],
    example_value=Literal('Example Value'),
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#EncodingConstraint",
)
encoding_constraint_base_characteristic.append_parent_element(encoding_constraint_characteristic)
encoding_constraint.append_parent_element(encoding_constraint_characteristic)

encoding_constraint_property = Property(
    name="encodingConstraintProperty",
    preferred_names={'en': 'Test Property'},
    descriptions={'en': 'This is a test property.'},
    meta_model_version="2.1.0",
    see=['http://example.com/', 'http://example.com/me'],
    characteristic=encoding_constraint_characteristic,
    example_value=Literal('Example Value'),
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#testProperty",
)
encoding_constraint_characteristic.append_parent_element(encoding_constraint_property)

aspect = Aspect(
    name="AspectWithEncodingConstraint",
    preferred_names={'en': 'Test Aspect'},
    descriptions={'en': 'This is a test description'},
    meta_model_version="2.1.0",
    see=['http://example.com/'],
    properties=[encoding_constraint_property],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#AspectWithEncodingConstraint",
)
encoding_constraint_property.append_parent_element(aspect)

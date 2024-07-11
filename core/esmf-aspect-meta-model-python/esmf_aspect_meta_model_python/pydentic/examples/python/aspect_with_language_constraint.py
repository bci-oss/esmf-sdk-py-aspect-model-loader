"""Example for the Aspect model with language constraint.

model: pydentic\examples\models\samm_2_1_0\org.eclipse.esmf.test\1.0.0\AspectWithLanguageConstraint.ttl
"""

from rdflib.term import Literal

from esmf_aspect_meta_model_python.pydentic.meta_model_elements.aspect import Aspect
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.property import Property
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.scalar import Scalar
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.trait import Trait
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.constraints.language_constraint import LanguageConstraint


language_constraint_base_characteristic = Characteristic(
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
        urn=" http://www.w3.org/2001/XMLSchema#string",
    ),
    urn="urn:samm:org.eclipse.esmf.samm:characteristic:2.1.0#Text",
)

language_constraint = LanguageConstraint(
    name="LanguageConstraintCharacteristic_constraint",
    preferred_names={'en': 'Test Language Constraint'},
    descriptions={'en': 'This is a test language constraint.'},
    meta_model_version="2.1.0",
    see=['http://example.com/'],
    language_code="de",
)

language_constraint_characteristic = Trait(
    name="LanguageConstraintCharacteristic",
    meta_model_version="2.1.0",
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#string",
    ),
    base_characteristic=language_constraint_base_characteristic,
    constraints=[language_constraint],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#LanguageConstraintCharacteristic",
)
language_constraint_base_characteristic.append_parent_element(language_constraint_characteristic)
language_constraint.append_parent_element(language_constraint_characteristic)

language_constraint_property = Property(
    name="languageConstraintProperty",
    preferred_names={'en': 'Test Property'},
    descriptions={'en': 'This is a test property.'},
    meta_model_version="2.1.0",
    see=['http://example.com/', 'http://example.com/me'],
    characteristic=language_constraint_characteristic,
    example_value=Literal("Example Value"),
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#languageConstraintProperty",
)
language_constraint_characteristic.append_parent_element(language_constraint_property)

aspect = Aspect(
    name="AspectWithLanguageConstraint",
    preferred_names={'en': 'Test Aspect'},
    descriptions={'en': 'This is a test description'},
    meta_model_version="2.1.0",
    see=['http://example.com/'],
    properties=[language_constraint_property],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#AspectWithLanguageConstraint",
)
language_constraint_property.append_parent_element(aspect)

"""Example for the Aspect model with collection list of scalar elements.

model: pydentic\examples\models\samm_2_1_0\org.eclipse.esmf.test\1.0.0\AspectWithCollection.ttl
"""

from rdflib.term import Literal

from esmf_aspect_meta_model_python.pydentic.meta_model_elements.aspect import Aspect
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.property import Property
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.collection.collection import Collection
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.scalar import Scalar


collection_characteristic = Collection(
    name="TestCollection",
    preferred_names={'en': 'Test Collection'},
    descriptions={'en': 'This is a test collection.'},
    meta_model_version="2.1.0",
    see=["<http://example.com/>"],
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#string",
    ),
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#TestCollection",
)

collection_property = Property(
    name="collectionProperty",
    preferred_names={'en': 'Test Property'},
    descriptions={'en': 'This is a test property.'},
    meta_model_version="2.1.0",
    see=["<http://example.com/>", "<http://example.com/me>"],
    example_value=Literal("Example Value"),
    characteristic=collection_characteristic,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#testProperty",
)
collection_characteristic.append_parent_element(collection_property)

aspect = Aspect(
    name="AspectWithCollection",
    preferred_names={'en': 'Test Aspect'},
    descriptions={'en': 'This is a test description'},
    meta_model_version="2.1.0",
    see=["<http://example.com/>"],
    properties=[collection_property],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#AspectWithCollection",
)
collection_property.append_parent_element(aspect)

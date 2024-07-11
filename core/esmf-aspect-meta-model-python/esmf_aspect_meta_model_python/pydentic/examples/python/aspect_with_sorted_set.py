"""Example for the Aspect model with collection sorted set.

model: pydentic\examples\models\samm_2_1_0\org.eclipse.esmf.test\1.0.0\AspectWithSortedSet.ttl
"""

from rdflib.term import Literal

from esmf_aspect_meta_model_python.pydentic.meta_model_elements.aspect import Aspect
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.property import Property
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.collection.sorted_set import SortedSet
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.scalar import Scalar


sorted_set_collection_characteristic = SortedSet(
    name="sortedSetCollection",
    preferred_names={"en": "Test Sorted Set"},
    descriptions={"en": "This is a test sorted set."},
    meta_model_version="2.1.0",
    see="<http://example.com/>",
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#string",
    ),
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#sortedSetCollection",
)

sorted_set_collection_property = Property(
    name="sortedSetCollectionProperty",
    preferred_names={"en": "Test Property"},
    descriptions={"en": "This is a test property."},
    meta_model_version="2.1.0",
    see=["<http://example.com/>", "<http://example.com/me>"],
    example_value=Literal("Example Value"),
    characteristic=sorted_set_collection_characteristic,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#sortedSetCollectionProperty",
)
sorted_set_collection_characteristic.append_parent_element(sorted_set_collection_property)

aspect = Aspect(
    name="AspectWithSortedSet",
    preferred_names={"en": "Test Aspect"},
    descriptions={"en": "This is a test description"},
    meta_model_version="2.1.0",
    see=["<http://example.com/>"],
    properties=[sorted_set_collection_property],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#AspectWithSortedSet",
)
sorted_set_collection_property.append_parent_element(aspect)

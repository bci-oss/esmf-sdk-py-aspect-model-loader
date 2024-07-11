"""Example for the Aspect model with collections: list and set.

model: pydentic\examples\models\samm_2_1_0\org.eclipse.esmf.test\1.0.0\AspectWithCollections.ttl
"""

from esmf_aspect_meta_model_python.pydentic.meta_model_elements.aspect import Aspect
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.property import Property
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.collection.list import List
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.collection.set import Set
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.scalar import Scalar


list_property = Property(
    name="listProperty",
    meta_model_version="2.1.0",
    characteristic=List(
        name="listProperty_characteristic",
        data_type=Scalar(
            meta_model_version="",
            urn="http://www.w3.org/2001/XMLSchema#string",
            is_scalar=True,
            is_complex=False,
        ),
    ),
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#listProperty",
)
list_property.characteristic.append_parent_element(list_property)

set_property = Property(
    name="setProperty",
    meta_model_version="2.1.0",
    characteristic=Set(
        name="setProperty_characteristic",
        data_type=Scalar(
            meta_model_version="2.1.0",
            urn="http://www.w3.org/2001/XMLSchema#string",
            is_scalar=True,
            is_complex=False,
        ),
    ),
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#setProperty",
)
set_property.characteristic.append_parent_element(set_property)

aspect = Aspect(
    name="AspectWithCollections",
    meta_model_version="2.1.0",
    properties=[set_property, list_property],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#AspectWithCollections",
)
set_property.append_parent_element(aspect)
list_property.append_parent_element(aspect)

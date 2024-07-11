"""Example for the Aspect model.

model: pydentic/examples/models/samm_2_1_0/org.eclipse.esmf.test/1.0.0/Aspect.ttl
"""

from esmf_aspect_meta_model_python.pydentic.meta_model_elements.aspect import Aspect


aspect = Aspect(
    name="Aspect",
    preferred_names={'en': "Test Aspect"},
    descriptions={'en': "This is a test description"},
    see=[],
    meta_model_version="2.1.0",
    properties=[],
    operations=[],
    events=[],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#Aspect",
    parent_elements=None,
    is_collection_aspect=False,
)

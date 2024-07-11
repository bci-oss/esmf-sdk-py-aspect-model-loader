"""Example for the Aspect model with collection time series.

model: pydentic\examples\models\samm_2_1_0\org.eclipse.esmf.test\1.0.0\AspectWithTimeSeries.ttl
"""

from esmf_aspect_meta_model_python.pydentic.meta_model_elements.aspect import Aspect
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.property import Property
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.collection.time_series import TimeSeries
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.entity import Entity
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.scalar import Scalar


entity_characteristic = Characteristic(
    name="Text",
    preferred_names={'en': 'Text'},
    descriptions={
        'en': (
            'Describes a Property which contains plain text. This is intended exclusively for human readable strings, '
            'not for identifiers, measurement values, etc.'
        ),
    },
    meta_model_version="2.1.0",
    data_type=Scalar(
        meta_model_version="2.1.0",
        urn="http://www.w3.org/2001/XMLSchema#string",
    ),
    urn="urn:samm:org.eclipse.esmf.samm:characteristic:2.1.0#Text",
)

extend_property = Property(
    name="value",
    preferred_names={'en': 'Value'},
    descriptions={'en': 'The value that was recorded and is part of a time series.'},
    meta_model_version="2.1.0",
    urn="urn:samm:org.eclipse.esmf.samm:entity:2.1.0#value",
)

entity_property = Property(
    name="extending_value",
    meta_model_version="2.1.0",
    characteristic=entity_characteristic,
    extends=extend_property,
)
entity_characteristic.append_parent_element(entity_property)
extend_property.append_parent_element(entity_property)

time_series_entity = Entity(
    name="TimeSeriesEntity",
    preferred_names={'en': 'Test Time Series Entity'},
    descriptions={'en': 'This is a test time series entity.'},
    see=['http://example.com/'],
    meta_model_version="2.1.0",
    properties=[extend_property],
    extends_urn="urn:samm:org.eclipse.esmf.samm:entity:2.1.0#TimeSeriesEntity",
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#TestTimeSeriesEntity",
)
entity_property.append_parent_element(time_series_entity)

time_series_collection_characteristic = TimeSeries(
    name="TimeSeriesCollection",
    preferred_names={"en": "Test Time Series"},
    descriptions={"en": "This is a test time series."},
    meta_model_version="2.1.0",
    see="<http://example.com/>",
    data_type=time_series_entity,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#TimeSeriesCollection",
)
time_series_entity.append_parent_element(time_series_collection_characteristic)

time_series_collection_property = Property(
    name="timeSeriesCollectionProperty",
    preferred_names={"en": "Test Property"},
    descriptions={"en": "This is a test property."},
    meta_model_version="2.1.0",
    see=["<http://example.com/>", "<http://example.com/me>"],
    characteristic=time_series_collection_characteristic,
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#timeSeriesCollectionProperty",
)
time_series_collection_characteristic.append_parent_element(time_series_collection_property)

aspect = Aspect(
    name="AspectWithTimeSeries",
    preferred_names={"en": "Test Aspect"},
    descriptions={"en": "This is a test description"},
    meta_model_version="2.1.0",
    see=["<http://example.com/>"],
    properties=[time_series_collection_property],
    urn="urn:samm:org.eclipse.esmf.test:1.0.0#AspectWithTimeSeries",
)
time_series_collection_property.append_parent_element(aspect)

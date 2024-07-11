"""Example of the Aspect class.

Create data classes for representation from Aspect Model
"""

from pydantic import BaseModel
from typing import Optional

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.event import Event
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.operation import Operation
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.property import Property


class Aspect(BaseModel):
    """Aspect class.

    :param name: Aspect name.
    :param preferred_names: Human-readable name in a specific language.
        This attribute may be defined multiple times for different languages but only once for a specific language.
        There should be at least one preferredName defined with an "en" language tag.
    :param descriptions: Human-readable description in a specific language.
        This attribute may be defined multiple times for different languages but only once for a specific language.
        There should be at least one description defined with an "en" language tag.
    :param see: A reference to a related element in an external taxonomy, ontology or other standards document.
    :param meta_model_version: A version of the model element. Required
    :param properties: The list of Properties of this Aspect.
    :param operations: The list of Operations of this Aspect.
    :param events: The list of Events of this Aspect.
    :param urn: A uniform Identifier of the Aspect in the model.
    :param parent_elements: List of parent elements for the current Aspect in the model.
    :param is_collection_aspect: A flag to identify whether an instance is an aspect of a collection or not.
    """
    name: str = ""
    preferred_names: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    see: list[str] = []
    meta_model_version: str
    properties: list[Property] = []
    operations: list[Operation] = []
    events: list[Event] = []
    urn: Optional[str] = None
    parent_elements: list[BaseModel] = []
    is_collection_aspect: bool = False

    def get_preferred_name(self, locale: str) -> Optional[str]:
        """Gets preferred name."""
        return self.preferred_names.get(locale)

    def get_description(self, locale: str) -> Optional[str]:
        """Gets description in specified language."""
        return self.descriptions.get(locale)

    def append_parent_element(self, element: Base) -> None:
        """Extend parent_elements list."""
        self._parent_elements.append(element)

    def _set_parent_element_on_child_elements(self) -> None:
        """Set a parent element on child elements."""
        for aspect_property in self._properties:
            aspect_property.append_parent_element(self)

        for operation in self._operations:
            operation.append_parent_element(self)

        for event in self._events:
            event.append_parent_element(self)


def test_aspect_default_values():
    aspect = Aspect(meta_model_version="0.0.0")

    assert aspect.name == ""
    assert aspect.preferred_names == {}
    assert aspect.descriptions == {}
    assert aspect.see == []
    assert aspect.meta_model_version == "0.0.0"
    assert aspect.properties == []
    assert aspect.operations == []
    assert aspect.events == []
    assert aspect.urn is None
    assert aspect.parent_elements == []
    assert not aspect.is_collection_aspect


def test_aspect_attributes():
    property_one = Property(name="PropertyOne")
    operation_one = Operation(name="OperationOne")
    event_one = Event(name="EventOne")
    aspect = Aspect(
        name="Aspect name",
        preferred_names={"en": "Aspect preferred name"},
        descriptions={"en": "Aspect description"},
        see=["link_to_external_document"],
        meta_model_version="0.0.1",
        properties=[property_one],
        operations=[operation_one],
        events=[event_one],
        urn="urn.to.Aspect#0.01",
    )

    assert aspect.name == "Aspect name"
    assert aspect.get_preferred_name("en") == "Aspect preferred name"
    assert aspect.get_description("en") == "Aspect description"
    assert aspect.see == ["link_to_external_document"]
    assert aspect.meta_model_version == "0.0.1"
    assert aspect.properties == [property_one]
    assert aspect.operations == [operation_one]
    assert aspect.events == [event_one]
    assert aspect.urn == "urn.to.Aspect#0.01"
    assert aspect.parent_elements == []
    assert not aspect.is_collection_aspect


def all_tests():
    test_aspect_default_values()
    test_aspect_attributes()

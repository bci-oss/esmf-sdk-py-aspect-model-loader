"""Example of the Aspect class.

Create data classes for representation from Aspect Model (we'll look into Pydantic)
"""

from pydantic import BaseModel
from typing import Optional

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.pydentic.elements.event import Event
from esmf_aspect_meta_model_python.pydentic.elements.operation import Operation
from esmf_aspect_meta_model_python.pydentic.elements.property import Property


class Aspect(BaseModel):
    name: str                             # can be ""
    preferred_names: dict[str, str]       # can be {}
    descriptions: dict[str, str]          # can be {}
    see: list[str]                        # can be []
    meta_model_version: str               # can be ""
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

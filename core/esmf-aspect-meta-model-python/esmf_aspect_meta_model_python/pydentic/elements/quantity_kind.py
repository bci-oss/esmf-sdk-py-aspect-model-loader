"""Example of the QuantityKind class.

Create data classes for representation from Aspect Model (we'll look into Pydantic)
"""

from pydantic import BaseModel
from typing import Optional

from esmf_aspect_meta_model_python.base.base import Base


class QuantityKind(BaseModel):
    name: str  # can be ""
    preferred_names: dict[str, str]  # can be {}
    descriptions: dict[str, str]  # can be {}
    see: list[str]  # can be []
    meta_model_version: str  # can be ""
    urn: Optional[str] = None
    parent_elements: list[BaseModel] = []

    def get_preferred_name(self, locale: str) -> Optional[str]:
        """Gets preferred name."""
        return self.preferred_names.get(locale)

    def get_description(self, locale: str) -> Optional[str]:
        """Gets description in specified language."""
        return self.descriptions.get(locale)

    def append_parent_element(self, element: Base) -> None:
        """Extend parent_elements list."""
        self._parent_elements.append(element)

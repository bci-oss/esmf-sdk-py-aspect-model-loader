"""Example of the Unit class.

Create data classes for representation from Aspect Model (we'll look into Pydantic)
"""

from pydantic import BaseModel
from typing import Optional, Set

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.pydentic.elements.quantity_kind import QuantityKind


class Unit(BaseModel):
    name: str                        # can be ""
    preferred_names: dict[str, str]  # can be {}
    descriptions: dict[str, str]     # can be {}
    see: list[str]                   # can be []
    meta_model_version: str          # can be ""
    urn: Optional[str] = None
    parent_elements: list[BaseModel] = []
    symbol: Optional[str] = None
    code: Optional[str] = None
    reference_unit: Optional[str] = None
    conversion_factor: Optional[str] = None
    quantity_kinds = Set[QuantityKind]

    def get_preferred_name(self, locale: str) -> Optional[str]:
        """Gets preferred name."""
        return self.preferred_names.get(locale)

    def get_description(self, locale: str) -> Optional[str]:
        """Gets description in specified language."""
        return self.descriptions.get(locale)

    def append_parent_element(self, element: Base) -> None:
        """Extend parent_elements list."""
        self._parent_elements.append(element)

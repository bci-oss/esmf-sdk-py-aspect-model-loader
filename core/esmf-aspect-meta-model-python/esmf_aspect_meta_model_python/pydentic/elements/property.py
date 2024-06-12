"""Example of the Property class.

Create data classes for representation from Aspect Model (we'll look into Pydantic)
"""

from pydantic import BaseModel, StrictBool
from typing import Any, Optional

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.pydentic.elements.characteristic import Characteristic
from esmf_aspect_meta_model_python.pydentic.elements.data_type import DataType
from esmf_aspect_meta_model_python.pydentic.elements.trait import Trait


class Property(BaseModel):
    name: str                        # can be ""
    preferred_names: dict[str, str]  # can be {}
    descriptions: dict[str, str]     # can be {}
    see: list[str]                   # can be []
    meta_model_version: str          # can be ""
    urn: Optional[str] = None
    parent_elements: list[BaseModel] = []
    characteristic: Optional[Characteristic] = None
    example_value: Optional[Any] = None
    extends: Optional["Property"] = None
    is_abstract: StrictBool = False
    is_optional: StrictBool = False
    is_not_in_payload: StrictBool = False
    payload_name: Optional[str] = None
    data_type: Optional[DataType]

    def get_preferred_name(self, locale: str) -> Optional[str]:
        """Gets preferred name."""
        return self.preferred_names.get(locale)

    def get_description(self, locale: str) -> Optional[str]:
        """Gets description in specified language."""
        return self.descriptions.get(locale)

    def append_parent_element(self, element: Base) -> None:
        """Extend parent_elements list."""
        self._parent_elements.append(element)

    def data_type(self) -> Optional[DataType]:
        """Data type."""
        return self.effective_characteristic.data_type if self.effective_characteristic else None

    @property
    def effective_characteristic(self) -> Optional[Characteristic]:
        """Effective characteristic."""
        characteristic = None

        if self.characteristic:
            characteristic = self.characteristic
            while isinstance(characteristic, Trait):
                characteristic = characteristic.base_characteristic

        return characteristic

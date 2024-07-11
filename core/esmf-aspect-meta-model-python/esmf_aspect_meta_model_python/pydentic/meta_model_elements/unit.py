"""Example of the Unit class.

Create data classes for representation from Aspect Model
"""

from pydantic import BaseModel
from typing import Optional, Set

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.quantity_kind import QuantityKind


class Unit(BaseModel):
    """Unit interface class.

    A unit is used to specify the magnitude of a physical quantity.
    Examples for units are meter, millimeter, inch, or volts. A Unit in the SAMM.

    :param name: Aspect name.
    :param preferred_names: Human-readable name in a specific language.
        This attribute may be defined multiple times for different languages but only once for a specific language.
        There should be at least one preferredName defined with an "en" language tag.
    :param descriptions: Human-readable description in a specific language.
        This attribute may be defined multiple times for different languages but only once for a specific language.
        There should be at least one description defined with an "en" language tag.
    :param see: A reference to a related element in an external taxonomy, ontology or other standards document.
    :param meta_model_version: A version of the model element. Required
    :param urn: A uniform Identifier of the Aspect in the model.
    :param parent_elements: List of parent elements for the current Aspect in the model.
    :param symbol: Symbol of the unit.
    :param code: Code of the unit.
    :param reference_unit: Referenced unit.
    :param conversion_factor: A conversion factor.
    :param quantity_kinds: A set of the quantity kinds for the unit.
    """
    name: str = ""
    preferred_names: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    see: list[str] = []
    meta_model_version: str = ""
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

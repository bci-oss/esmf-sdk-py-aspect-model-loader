"""Example of the FixedPointConstraint class.

Create data classes for representation from Aspect Model
"""

from pydantic import BaseModel
from typing import Optional

from esmf_aspect_meta_model_python.base.base import Base


class FixedPointConstraint(BaseModel):
    """Constraint interface class.

    A constraint restricts a characteristic in a certain way.
    Constraints are wrapped in a Trait which holds a reference to the actual characteristic.

    :param name: Collection node name.
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
    :param scale: The scaling factor for a fixed point number. E.g., if a fixedpoint number is 123.04, the scaling
        factor is 2 (the number of digits after the decimal point).
    :param integer: The number of integral digits for a fixed point number. E.g., if a fixedpoint number is 123.04,
        the integer factor is 3 (the number of digits before the decimal point).
    """
    name: str = ""
    preferred_names: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    see: list[str] = []
    meta_model_version: str
    urn: Optional[str] = None
    parent_elements: list[BaseModel] = []
    scale: int
    integer: int

    def get_preferred_name(self, locale: str) -> Optional[str]:
        """Gets preferred name."""
        return self.preferred_names.get(locale)

    def get_description(self, locale: str) -> Optional[str]:
        """Gets description in specified language."""
        return self.descriptions.get(locale)

    def append_parent_element(self, element: Base) -> None:
        """Extend parent_elements list."""
        self._parent_elements.append(element)

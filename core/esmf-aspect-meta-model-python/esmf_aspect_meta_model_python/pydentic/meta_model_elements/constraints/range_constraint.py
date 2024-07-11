"""Example of the RangeConstraint class.

Create data classes for representation from Aspect Model
"""

from pydantic import BaseModel
from typing import Any, Optional

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.bound_definition import (
    LowBoundDefinition,
    UpperBoundDefinition,
)


class RangeConstraint(BaseModel):
    """Range Constraint interface class.

    Restricts the value range of a Property.
    At least one of samm-c:maxValue or samm-c:minValue must be present in a Range Constraint.
    Additionally, the Bound Definition can specify whether the upper and lower value are included in the range.

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
    :param min_value: The lower bound of a range.
    :param min_value: The upper bound of a range.
    :param lower_bound_definition: Defines whether the lower bound of a range is inclusive or exclusive.
    :param upper_bound_definition: Defines whether the upper bound of a range is inclusive or exclusive.
    """


    name: str = ""
    preferred_names: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    see: list[str] = []
    meta_model_version: str
    urn: Optional[str] = None
    parent_elements: list[BaseModel] = []
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    lower_bound_definition: Optional[LowBoundDefinition] = None
    upper_bound_definition: Optional[UpperBoundDefinition] = None

    def get_preferred_name(self, locale: str) -> Optional[str]:
        """Gets preferred name."""
        return self.preferred_names.get(locale)

    def get_description(self, locale: str) -> Optional[str]:
        """Gets description in specified language."""
        return self.descriptions.get(locale)

    def append_parent_element(self, element: Base) -> None:
        """Extend parent_elements list."""
        self._parent_elements.append(element)

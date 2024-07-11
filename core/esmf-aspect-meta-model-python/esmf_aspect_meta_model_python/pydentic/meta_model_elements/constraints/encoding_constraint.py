"""Example of the EncodingConstraint class.

Create data classes for representation from Aspect Model
"""

from pydantic import BaseModel
from typing import Optional

from esmf_aspect_meta_model_python.base.base import Base


class EncodingConstraint(BaseModel):
    """Encoding Constraint interface class.

    Restricts the encoding of a Property. e.g. samm:UTF-8, samm:US:ASCII.

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
    :param value: Configures the encoding. This must be one of the following: samm:US-ASCII, samm:ISO-8859-1,
        samm:UTF-8, samm:UTF-16, samm:UTF-16BE or samm:UTF-16LE.
    """
    name: str = ""
    preferred_names: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    see: list[str] = []
    meta_model_version: str
    urn: Optional[str] = None
    parent_elements: list[BaseModel] = []
    value: str

    def get_preferred_name(self, locale: str) -> Optional[str]:
        """Gets preferred name."""
        return self.preferred_names.get(locale)

    def get_description(self, locale: str) -> Optional[str]:
        """Gets description in specified language."""
        return self.descriptions.get(locale)

    def append_parent_element(self, element: Base) -> None:
        """Extend parent_elements list."""
        self._parent_elements.append(element)

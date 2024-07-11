"""Example of the ComplexType class.

Create data classes for representation from Aspect Model (we'll look into Pydantic)
"""

from pydantic import BaseModel, StrictBool
from typing import ForwardRef, Optional

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.property import Property


ComplexType = ForwardRef('ComplexType')


class ComplexType(BaseModel):
    """Complex Type interface class.

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
    :param properties: The list of Properties which make up the Entity.
    :param is_abstract_entity: Flag indicate weather the class can be instantiated or not.
    :param is_complex: Flag indicate weather the DataType is complex or not.
    :param is_scalar: Flag indicate weather the DataType is scalar or not.
    :param extends: The Entity which is extended by this Entity.
    """
    _instances: dict[str, ComplexType] = {}

    name: str = ""
    preferred_names: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    see: list[str] = []
    meta_model_version: str = ""
    urn: Optional[str] = None
    parent_elements: list[BaseModel] = []
    properties: list[Property] = []
    is_abstract_entity: StrictBool = True
    is_complex: StrictBool = True
    is_scalar: StrictBool = False
    extends: Optional[str] = None

    def get_preferred_name(self, locale: str) -> Optional[str]:
        """Gets preferred name."""
        return self.preferred_names.get(locale)

    def get_description(self, locale: str) -> Optional[str]:
        """Gets description in specified language."""
        return self.descriptions.get(locale)

    def append_parent_element(self, element: Base) -> None:
        """Extend parent_elements list."""
        self._parent_elements.append(element)

    @property
    def all_properties(self) -> list[Property]:
        """All properties including properties from the extended element."""
        properties = self.properties[:]

        if self.extends:
            node = self._instances.get(self.extends)
            properties.extend(node.all_properties)

        return properties

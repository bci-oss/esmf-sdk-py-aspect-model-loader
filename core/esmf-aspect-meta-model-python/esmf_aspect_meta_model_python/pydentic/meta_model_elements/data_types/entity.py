"""Example of the Entity class.

Create data classes for representation from Aspect Model
"""

from pydantic import BaseModel, StrictBool
from typing import Optional

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.property import Property
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.complex_type import ComplexType


class Entity(BaseModel):
    """Entity interface class.

    Complex Data Type that includes a number of properties.
    An Entity specifies a value that can't be expressed by a scalar e.g. a vector.

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
    name: str = ""
    preferred_names: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    see: list[str] = []
    meta_model_version: str
    urn: Optional[str] = None
    parent_elements: list[BaseModel] = []
    properties: list[Property] = []
    is_abstract_entity: StrictBool = False
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
        """All properties."""
        if self.extends_urn is None:
            return self.properties

        properties: list[Property] = []
        properties.extend(self.__properties)
        if self.extends is not None:
            properties.extend(self.extends.all_properties)
        return properties

    @property
    def extends(self) -> Optional[ComplexType]:
        """Extends."""
        try:
            if self.extends_urn is None:
                return None
            return self._instances[self.extends_urn]
        except KeyError:
            return None

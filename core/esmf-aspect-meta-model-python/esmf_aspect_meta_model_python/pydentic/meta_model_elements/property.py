"""Example of the Property class.

Create data classes for representation from Aspect Model
"""

from pydantic import BaseModel, StrictBool
from typing import Any, Optional

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.data_types.data_type import DataType
from esmf_aspect_meta_model_python.pydentic.meta_model_elements.characteristics.trait import Trait


class Property(BaseModel):
    """Property class.

    :param name: Property name.
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
    :param characteristic: The Characteristic describing this Property.
    :param example_value: An exemplary value the Property can take on that helps to understand the intended meaning
        of the property better.
    :param extends: The Property which is extended by this Property.
    :param is_abstract: A flag to identify whether the Property is an abstract or not.
    :param is_optional: A flag to identify whether the Property is an optional or not.
    :param is_not_in_payload: A flag to identify whether the Property is not in payload or not.
    :param payload_name: Name in the runtime payload. Uses as a key of the Property in the runtime payload
        This allows for the separation of the semantic name of the Property and the corresponding key.
    """
    name: str = ""
    preferred_names: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    see: list[str] = []
    meta_model_version: str
    urn: Optional[str] = None
    parent_elements: list[BaseModel] = []
    characteristic: Optional[Characteristic] = None
    example_value: Optional[Any] = None
    extends: Optional["Property"] = None
    is_abstract: StrictBool = False
    is_optional: StrictBool = False
    is_not_in_payload: StrictBool = False
    payload_name: Optional[str] = None

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
    def effective_characteristic(self) -> Optional[Characteristic]:
        """Effective characteristic."""
        characteristic = None

        if self.characteristic:
            characteristic = self.characteristic
            while isinstance(characteristic, Trait):
                characteristic = characteristic.base_characteristic

        return characteristic

    @property
    def data_type(self) -> Optional[DataType]:
        """Data type."""
        return self.effective_characteristic.data_type if self.effective_characteristic else None


def test_property_default_values():
    test_property = Property(meta_model_version="0.0.0")

    assert test_property.name == ""
    assert test_property.preferred_names == {}
    assert test_property.descriptions == {}
    assert test_property.see == []
    assert test_property.meta_model_version == "0.0.0"
    assert test_property.urn is None
    assert test_property.parent_elements == []
    assert test_property.characteristic is None
    assert test_property.example_value is None
    assert test_property.extends is None
    assert not test_property.is_abstract
    assert not test_property.is_optional
    assert not test_property.is_not_in_payload
    assert test_property.payload_name is None
    assert test_property.data_type is None
    assert test_property.data_type is None
    assert test_property.effective_characteristic is None
    assert test_property.data_type is None


def test_property_attributes():
    from esmf_aspect_meta_model_python.pydentic.meta_model_elements.aspect import Aspect
    aspect = Aspect(name="Aspect", meta_model_version="0.0.1")
    characteristic_one = Characteristic(name="CharacteristicOne")
    data_type = DataType(name="int_data_type")
    test_property = Property(
        name="Property name",
        preferred_names={"en": "Property preferred name"},
        descriptions={"en": "Property description"},
        see=["link_to_external_document"],
        meta_model_version="0.0.1",
        urn="urn.to.Property#0.01",
        parent_elements=[aspect],
        characteristic=[characteristic_one],
        example_value=1,
        payload_name='payload_one',
        data_type=data_type,
    )

    assert test_property.name == "Property name"
    assert test_property.preferred_names == {"en": "Test Property"}
    assert test_property.descriptions == {"en": "Property description"}
    assert test_property.see == ["link_to_external_document"]
    assert test_property.meta_model_version == "0.0.1"
    assert test_property.urn == "urn.to.Property#0.01"
    assert test_property.parent_elements == [aspect]
    assert test_property.characteristic == [characteristic_one]
    assert test_property.example_value == 1
    assert test_property.extends is None
    assert not test_property.is_abstract
    assert not test_property.is_optional
    assert not test_property.is_not_in_payload
    assert test_property.payload_name == "payload_one"
    assert test_property.data_type == data_type


def all_tests():
    test_property_default_values()
    test_property_attributes()

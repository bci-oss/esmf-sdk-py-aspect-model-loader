"""Example of the DataType class.

Create data classes for representation from Aspect Model
"""

from pydantic import BaseModel, StrictBool
from typing import Optional


class DataType(BaseModel):
    """Data Type interface class.

    A data type specifies the structure of the value a characteristic can have.
    Data types are classified in scalar (e.g. integer, string, etc.) and complex (Entity).

    :param meta_model_version: A version of the model element. Required
    :param urn: A uniform Identifier of the Aspect in the model.
    :param is_complex: Flag indicate weather the DataType is complex or not.
    :param is_scalar: Flag indicate weather the DataType is scalar or not.
    """
    meta_model_version: str  # can be ""
    urn: Optional[str] = None
    is_complex: StrictBool = True
    is_scalar: StrictBool = False

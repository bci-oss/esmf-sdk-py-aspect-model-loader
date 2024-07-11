"""Example of the Scalar data type class.

Create data classes for representation from Aspect Model
"""

from pydantic import BaseModel, StrictBool
from typing import Optional


class Scalar(BaseModel):
    """Scalar interface class.

    Simple data type that specifies a value. The type of the scalar is determined by the URN e.g.
    http://www.w3.org/2001/XMLSchema#integer for an integer value.

    :param meta_model_version: A version of the model element. Required
    :param urn: A uniform Identifier of the Aspect in the model.
    :param is_complex: Flag indicate weather the DataType is complex or not.
    :param is_scalar: Flag indicate weather the DataType is scalar or not.
    """
    meta_model_version: str
    urn: Optional[str] = None
    is_complex: StrictBool = False
    is_scalar: StrictBool = True

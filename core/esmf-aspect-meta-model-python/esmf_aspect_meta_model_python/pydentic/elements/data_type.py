"""Example of the DataType class.

Create data classes for representation from Aspect Model (we'll look into Pydantic)
"""

from pydantic import BaseModel, StrictBool
from typing import Optional


class DataType(BaseModel):
    meta_model_version: str  # can be ""
    urn: Optional[str] = None
    is_complex: StrictBool = True
    is_scalar: StrictBool = False

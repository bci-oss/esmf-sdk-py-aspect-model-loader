"""Example of the BoundDefinition class.

Create data classes for representation from Aspect Model (we'll look into Pydantic)
"""
import enum

from pydantic import BaseModel


class BoundDefinition(BaseModel, enum.Enum):
    """Range Constraint interface class.

    Restricts the value range of a Property.
    At least one of samm-c:maxValue or samm-c:minValue must be present in a Range Constraint.
    Additionally, the Bound Definition can specify whether the upper and lower value are included in the range.
    """
    OPEN = "OPEN"
    AT_LEAST = "AT_LEAST"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"
    AT_MOST = "AT_MOST"


class LowBoundDefinition(str, enum.Enum):
    """Low Constraint of range."""
    AT_LEAST = "AT_LEAST"
    GREATER_THAN = "GREATER_THAN"


class UpperBoundDefinition(str, enum.Enum):
    """Low Constraint of range."""
    AT_LEAST = "AT_MOST"
    GREATER_THAN = "LESS_THAN"

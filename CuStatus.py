# Imports
from enum import Enum, auto


class CuStatus(Enum):
    """
    Enumeration containing all the possible statuses of the CUs.

    This enumeration will be used in order to limit the use of statuses to display in the main GUI.
    """
    UNKNOWN = auto()
    HEALTHY = auto()
    UNHEALTHY = auto()

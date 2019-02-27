# Imports
from enum import Enum

class CuStatus(Enum):
    """
    Enumeration containing all the possible statuses of the CUs.

    This enumeration will be used in order to limit the use of statuses to display in the main GUI.
    """
    UNKNOWN = 1
    HEALTHY = 2
    UNHEALTHY = 3

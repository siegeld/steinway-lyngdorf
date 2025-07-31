"""Constants and enumerations for Steinway P100."""

from enum import Enum, IntEnum


class PowerState(IntEnum):
    """Power states."""

    OFF = 0
    ON = 1


class FeedbackLevel(IntEnum):
    """Feedback verbosity levels."""

    MINIMAL = 0  # Only respond to queries
    STATUS = 1  # Auto status updates
    ECHO = 2  # Echo commands + status


class Zone(Enum):
    """Zone identifiers."""

    MAIN = "MAIN"
    ZONE2 = "ZONE2"


# Protocol constants
COMMAND_PREFIX = "!"
RESPONSE_PREFIX = "!"
ECHO_PREFIX = "#"
COMMAND_TERMINATOR = "\r"
DEFAULT_TCP_PORT = 84
DEFAULT_BAUD_RATE = 115200

# Timeouts (seconds)
DEFAULT_TIMEOUT = 5.0
CONNECT_TIMEOUT = 10.0

# Command strings
POWER_ON_MAIN = "POWERONMAIN"
POWER_OFF_MAIN = "POWEROFFMAIN"
POWER_ON_ZONE2 = "POWERONZONE2"
POWER_OFF_ZONE2 = "POWEROFFZONE2"
POWER_QUERY = "POWER?"
POWER_QUERY_ZONE2 = "POWERZONE2?"

"""Steinway P100 Control Library."""

from pathlib import Path

from .device import SteinwayP100Device
from .connection import TCPConnection, SerialConnection
from .exceptions import SteinwayError, ConnectionError, CommandError
from .constants import PowerState, Zone, FeedbackLevel

# Read version from VERSION file
_version_file = Path(__file__).parent.parent.parent / "VERSION"
if _version_file.exists():
    __version__ = _version_file.read_text().strip()
else:
    __version__ = "0.1.0"  # Fallback version
__all__ = [
    "SteinwayP100Device",
    "TCPConnection",
    "SerialConnection",
    "SteinwayError",
    "ConnectionError",
    "CommandError",
    "PowerState",
    "Zone",
    "FeedbackLevel",
]

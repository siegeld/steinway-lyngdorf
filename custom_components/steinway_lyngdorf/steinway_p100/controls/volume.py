"""Volume control for Steinway P100."""

import logging
from typing import TYPE_CHECKING

from ..constants import Zone
from ..protocol import CommandBuilder, ResponseParser

if TYPE_CHECKING:
    from ..connection import BaseConnection


logger = logging.getLogger(__name__)


class VolumeControl:
    """Control volume of Steinway P100."""

    # Volume limits in dB
    MIN_VOLUME_DB = -99.9
    MAX_VOLUME_DB = 24.0
    DEFAULT_STEP_DB = 0.5

    def __init__(self, connection: "BaseConnection", zone: Zone = Zone.MAIN):
        self._connection = connection
        self._zone = zone
        self._is_zone2 = zone == Zone.ZONE2

    async def get(self) -> float:
        """
        Get current volume level.

        Returns:
            Volume in dB (-99.9 to +24.0)
        """
        if self._is_zone2:
            command = "ZVOL?"
        else:
            command = "VOL?"

        response = await self._connection.send_command(command)

        if self._is_zone2:
            # Parse zone 2 volume response
            return ResponseParser.parse_zone2_volume(response)
        else:
            return ResponseParser.parse_volume(response)

    async def set(self, volume_db: float) -> None:
        """
        Set volume to specific level.

        Args:
            volume_db: Volume in dB (-99.9 to +24.0)

        Raises:
            ValueError: If volume is out of range
        """
        if volume_db < self.MIN_VOLUME_DB or volume_db > self.MAX_VOLUME_DB:
            raise ValueError(
                f"Volume {volume_db} dB out of range "
                f"({self.MIN_VOLUME_DB} to {self.MAX_VOLUME_DB})"
            )

        if self._is_zone2:
            command = CommandBuilder.zone2_volume_set(volume_db)
        else:
            command = CommandBuilder.volume_set(volume_db)

        await self._connection.send_command(command)
        logger.info(f"Set {self._zone.value} volume to {volume_db} dB")

    async def up(self, step_db: float = DEFAULT_STEP_DB) -> None:
        """
        Increase volume by specified step.

        Args:
            step_db: Step size in dB (default: 0.5)
        """
        if step_db <= 0:
            raise ValueError("Step must be positive")

        if self._is_zone2:
            if step_db == self.DEFAULT_STEP_DB:
                # Use simple up command for default step
                command = "ZVOL+"
            else:
                # Use specific step command
                command = CommandBuilder.zone2_volume_up(step_db)
        else:
            if step_db == self.DEFAULT_STEP_DB:
                command = "VOL+"
            else:
                command = CommandBuilder.volume_up(step_db)

        await self._connection.send_command(command)

    async def down(self, step_db: float = DEFAULT_STEP_DB) -> None:
        """
        Decrease volume by specified step.

        Args:
            step_db: Step size in dB (default: 0.5)
        """
        if step_db <= 0:
            raise ValueError("Step must be positive")

        if self._is_zone2:
            if step_db == self.DEFAULT_STEP_DB:
                command = "ZVOL-"
            else:
                command = CommandBuilder.zone2_volume_down(step_db)
        else:
            if step_db == self.DEFAULT_STEP_DB:
                command = "VOL-"
            else:
                command = CommandBuilder.volume_down(step_db)

        await self._connection.send_command(command)

    async def mute(self) -> None:
        """Mute the audio."""
        if self._is_zone2:
            command = "ZMUTEON"
        else:
            command = "MUTEON"

        await self._connection.send_command(command)
        logger.info(f"Muted {self._zone.value}")

    async def unmute(self) -> None:
        """Unmute the audio."""
        if self._is_zone2:
            command = "ZMUTEOFF"
        else:
            command = "MUTEOFF"

        await self._connection.send_command(command)
        logger.info(f"Unmuted {self._zone.value}")

    async def toggle_mute(self) -> None:
        """Toggle mute state."""
        if self._is_zone2:
            command = "ZMUTE"
        else:
            command = "MUTE"

        await self._connection.send_command(command)

    async def is_muted(self) -> bool:
        """
        Check if audio is muted.

        Returns:
            True if muted, False otherwise
        """
        if self._is_zone2:
            command = "ZMUTE?"
        else:
            command = "MUTE?"

        response = await self._connection.send_command(command)

        if self._is_zone2:
            return ResponseParser.parse_zone2_mute(response)
        else:
            return ResponseParser.parse_mute(response)

    async def get_limits(self) -> tuple[float, float]:
        """
        Get volume limits.

        Returns:
            Tuple of (min_volume_db, max_volume_db)
        """
        # Could query MAXVOL? for actual max limit
        # For now return constants
        return (self.MIN_VOLUME_DB, self.MAX_VOLUME_DB)

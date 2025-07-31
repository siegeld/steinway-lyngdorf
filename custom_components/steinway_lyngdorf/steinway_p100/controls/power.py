"""Power control for Steinway P100."""

import logging
from typing import TYPE_CHECKING

from ..constants import Zone, PowerState
from ..protocol import CommandBuilder, ResponseParser

if TYPE_CHECKING:
    from ..connection import BaseConnection


logger = logging.getLogger(__name__)


class PowerControl:
    """Control power state of Steinway P100."""

    def __init__(self, connection: "BaseConnection", zone: Zone = Zone.MAIN):
        self._connection = connection
        self._zone = zone

    async def on(self) -> None:
        """Turn the device on."""
        command = CommandBuilder.power_on(self._zone)
        await self._connection.send_command(command)
        logger.info(f"Powered on {self._zone.value}")

    async def off(self) -> None:
        """Turn the device off."""
        command = CommandBuilder.power_off(self._zone)
        await self._connection.send_command(command)
        logger.info(f"Powered off {self._zone.value}")

    async def toggle(self) -> None:
        """Toggle power state."""
        current = await self.status()
        if current == PowerState.ON:
            await self.off()
        else:
            await self.on()

    async def status(self) -> PowerState:
        """Get current power state."""
        command = CommandBuilder.power_query(self._zone)
        response = await self._connection.send_command(command)

        if self._zone == Zone.MAIN:
            return ResponseParser.parse_power_status(response)
        else:
            return ResponseParser.parse_zone2_power_status(response)

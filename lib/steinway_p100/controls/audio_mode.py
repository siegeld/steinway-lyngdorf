"""Audio processing mode control for Steinway P100."""

import logging
from typing import TYPE_CHECKING, List, Optional, Union

from ..protocol import CommandBuilder, ResponseParser

if TYPE_CHECKING:
    from ..connection import BaseConnection


logger = logging.getLogger(__name__)


class AudioMode:
    """Represents an audio processing mode."""

    def __init__(self, index: int, name: str):
        self.index = index
        self.name = name

    def __repr__(self):
        return f"AudioMode({self.index}, '{self.name}')"

    def __str__(self):
        return f"{self.index}: {self.name}"


class AudioModeControl:
    """Control audio processing modes of Steinway P100."""

    def __init__(self, connection: "BaseConnection"):
        self._connection = connection
        self._modes_cache: Optional[List[AudioMode]] = None

    async def get_modes(self, force_refresh: bool = False) -> List[AudioMode]:
        """
        Get list of available audio processing modes.

        Args:
            force_refresh: Force refresh of mode list cache

        Returns:
            List of AudioMode objects
        """
        if self._modes_cache is None or force_refresh:
            response = await self._connection.send_command("AUDMODEL?")
            self._modes_cache = ResponseParser.parse_audio_mode_list(response)

        return self._modes_cache

    async def get_current(self) -> AudioMode:
        """
        Get currently selected audio processing mode.

        Returns:
            Currently selected AudioMode
        """
        response = await self._connection.send_command("AUDMODE?")
        index, name = ResponseParser.parse_audio_mode(response)
        return AudioMode(index, name)

    async def select(self, mode: Union[int, AudioMode]) -> None:
        """
        Select an audio processing mode.

        Args:
            mode: Mode index or AudioMode object
        """
        if isinstance(mode, AudioMode):
            index = mode.index
        else:
            index = mode

        command = CommandBuilder.audio_mode_select(index)
        await self._connection.send_command(command)
        logger.info(f"Selected audio mode {index}")

    async def select_by_name(self, name: str) -> None:
        """
        Select an audio mode by name.

        Args:
            name: Mode name (case insensitive partial match)

        Raises:
            ValueError: If no matching mode found
        """
        modes = await self.get_modes()
        name_lower = name.lower()

        # Try exact match first
        for mode in modes:
            if mode.name.lower() == name_lower:
                await self.select(mode)
                return

        # Try partial match
        matches = []
        for mode in modes:
            if name_lower in mode.name.lower():
                matches.append(mode)

        if len(matches) == 1:
            await self.select(matches[0])
        elif len(matches) > 1:
            names = [m.name for m in matches]
            raise ValueError(f"Multiple modes match '{name}': {names}")
        else:
            raise ValueError(f"No mode found matching '{name}'")

    async def next(self) -> None:
        """Select next audio processing mode."""
        await self._connection.send_command("AUDMODE+")

    async def previous(self) -> None:
        """Select previous audio processing mode."""
        await self._connection.send_command("AUDMODE-")

    async def get_audio_type(self) -> str:
        """
        Get current audio input type information.

        Returns:
            String describing current audio format (e.g., "Dolby Atmos 7.1.4")
        """
        response = await self._connection.send_command("AUDTYPE?")
        return ResponseParser.parse_audio_type(response)

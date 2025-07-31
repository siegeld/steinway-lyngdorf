"""Source control for Steinway P100."""

import logging
from typing import TYPE_CHECKING, List, Optional, Union

from ..protocol import CommandBuilder, ResponseParser

if TYPE_CHECKING:
    from ..connection import BaseConnection


logger = logging.getLogger(__name__)


class Source:
    """Represents a source input."""

    def __init__(self, index: int, name: str):
        self.index = index
        self.name = name

    def __repr__(self):
        return f"Source({self.index}, '{self.name}')"

    def __str__(self):
        return f"{self.index}: {self.name}"


class SourceControl:
    """Control source selection of Steinway P100."""

    def __init__(self, connection: "BaseConnection"):
        self._connection = connection
        self._sources_cache: Optional[List[Source]] = None

    async def get_sources(self, force_refresh: bool = False) -> List[Source]:
        """
        Get list of available sources.

        Args:
            force_refresh: Force refresh of source list cache

        Returns:
            List of Source objects
        """
        if self._sources_cache is None or force_refresh:
            response = await self._connection.send_command("SRCS?")
            self._sources_cache = ResponseParser.parse_source_list(response)

        return self._sources_cache

    async def get_current(self) -> Source:
        """
        Get currently selected source.

        Returns:
            Currently selected Source
        """
        response = await self._connection.send_command("SRC?")
        index = ResponseParser.parse_source_index(response)

        # Get source list to find the name
        sources = await self.get_sources()
        for source in sources:
            if source.index == index:
                return source

        # If not found in cache, return a basic source
        return Source(index, f"Source {index}")

    async def select(self, source: Union[int, Source]) -> None:
        """
        Select a source.

        Args:
            source: Source index or Source object
        """
        if isinstance(source, Source):
            index = source.index
        else:
            index = source

        command = CommandBuilder.source_select(index)
        await self._connection.send_command(command)
        logger.info(f"Selected source {index}")

    async def select_by_name(self, name: str) -> None:
        """
        Select a source by name.

        Args:
            name: Source name (case insensitive partial match)

        Raises:
            ValueError: If no matching source found
        """
        sources = await self.get_sources()
        name_lower = name.lower()

        # Try exact match first
        for source in sources:
            if source.name.lower() == name_lower:
                await self.select(source)
                return

        # Try partial match
        matches = []
        for source in sources:
            if name_lower in source.name.lower():
                matches.append(source)

        if len(matches) == 1:
            await self.select(matches[0])
        elif len(matches) > 1:
            names = [s.name for s in matches]
            raise ValueError(f"Multiple sources match '{name}': {names}")
        else:
            raise ValueError(f"No source found matching '{name}'")

    async def next(self) -> None:
        """Select next source in the list."""
        current = await self.get_current()
        sources = await self.get_sources()

        if not sources:
            return

        # Find current index in list
        current_idx = 0
        for i, source in enumerate(sources):
            if source.index == current.index:
                current_idx = i
                break

        # Select next (wrap around)
        next_idx = (current_idx + 1) % len(sources)
        await self.select(sources[next_idx])

    async def previous(self) -> None:
        """Select previous source in the list."""
        current = await self.get_current()
        sources = await self.get_sources()

        if not sources:
            return

        # Find current index in list
        current_idx = 0
        for i, source in enumerate(sources):
            if source.index == current.index:
                current_idx = i
                break

        # Select previous (wrap around)
        prev_idx = (current_idx - 1) % len(sources)
        await self.select(sources[prev_idx])

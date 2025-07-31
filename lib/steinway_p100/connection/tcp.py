"""TCP connection implementation for Steinway P100."""

import asyncio
import logging
from typing import Optional

from .base import BaseConnection
from ..constants import DEFAULT_TCP_PORT, CONNECT_TIMEOUT
from ..exceptions import ConnectionError


logger = logging.getLogger(__name__)


class TCPConnection(BaseConnection):
    """TCP/IP connection to Steinway P100."""
    
    def __init__(self, host: str, port: int = DEFAULT_TCP_PORT):
        super().__init__()
        self.host = host
        self.port = port
        
    async def connect(self) -> None:
        """Establish TCP connection to the device."""
        if self._connected:
            return
            
        try:
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port),
                timeout=CONNECT_TIMEOUT
            )
            self._connected = True
            
            # Start read loop
            self._read_task = asyncio.create_task(self._read_loop())
            
            logger.info(f"Connected to {self.host}:{self.port}")
            
        except asyncio.TimeoutError:
            raise ConnectionError(f"Connection timeout to {self.host}:{self.port}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect: {e}")
            
    async def disconnect(self) -> None:
        """Close TCP connection."""
        if not self._connected:
            return
            
        self._connected = False
        
        if self._read_task:
            self._read_task.cancel()
            try:
                await self._read_task
            except asyncio.CancelledError:
                pass
                
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()
            
        logger.info(f"Disconnected from {self.host}:{self.port}")
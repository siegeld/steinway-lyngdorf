"""Serial connection implementation for Steinway P100."""

import asyncio
import logging

try:
    import serial_asyncio
except ImportError:
    serial_asyncio = None

from .base import BaseConnection
from ..constants import DEFAULT_BAUD_RATE, CONNECT_TIMEOUT
from ..exceptions import ConnectionError


logger = logging.getLogger(__name__)


class SerialConnection(BaseConnection):
    """Serial (RS232) connection to Steinway P100."""

    def __init__(self, port: str, baudrate: int = DEFAULT_BAUD_RATE):
        super().__init__()
        self.port = port
        self.baudrate = baudrate

        if serial_asyncio is None:
            raise ImportError("pyserial-asyncio is required for serial connections")

    async def connect(self) -> None:
        """Establish serial connection to the device."""
        if self._connected:
            return

        try:
            self._reader, self._writer = await asyncio.wait_for(
                serial_asyncio.open_serial_connection(
                    url=self.port,
                    baudrate=self.baudrate,
                    bytesize=8,
                    parity="N",
                    stopbits=1,
                    xonxoff=False,
                    rtscts=False,
                ),
                timeout=CONNECT_TIMEOUT,
            )
            self._connected = True

            # Start read loop
            self._read_task = asyncio.create_task(self._read_loop())

            logger.info(f"Connected to {self.port} at {self.baudrate} baud")

        except asyncio.TimeoutError:
            raise ConnectionError(f"Connection timeout to {self.port}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect: {e}")

    async def disconnect(self) -> None:
        """Close serial connection."""
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

        logger.info(f"Disconnected from {self.port}")

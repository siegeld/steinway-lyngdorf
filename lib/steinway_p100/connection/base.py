"""Base connection class for Steinway P100."""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Optional, Callable

from ..constants import (
    COMMAND_PREFIX, COMMAND_TERMINATOR, RESPONSE_PREFIX, 
    ECHO_PREFIX, DEFAULT_TIMEOUT, FeedbackLevel
)
from ..exceptions import ConnectionError, TimeoutError


logger = logging.getLogger(__name__)


class BaseConnection(ABC):
    """Abstract base class for Steinway P100 connections."""
    
    def __init__(self):
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._connected = False
        self._feedback_level = FeedbackLevel.STATUS
        self._response_handler: Optional[Callable] = None
        self._read_task: Optional[asyncio.Task] = None
        self._monitor_callback: Optional[Callable[[str, str], None]] = None
        
    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the device."""
        pass
        
    @abstractmethod
    async def disconnect(self) -> None:
        """Close the connection."""
        pass
        
    @property
    def is_connected(self) -> bool:
        """Check if connection is active."""
        return self._connected
        
    async def send_command(self, command: str, timeout: float = DEFAULT_TIMEOUT) -> Optional[str]:
        """
        Send a command and optionally wait for response.
        
        Args:
            command: Command string (without prefix/terminator)
            timeout: Response timeout in seconds
            
        Returns:
            Response string if query command, None otherwise
        """
        if not self._connected:
            raise ConnectionError("Not connected")
            
        # Build full command
        full_command = f"{COMMAND_PREFIX}{command}{COMMAND_TERMINATOR}"
        logger.debug(f"Sending: {full_command.strip()}")
        
        # Notify monitor if set
        if self._monitor_callback:
            self._monitor_callback("TX", full_command.strip())
        
        # Send command
        self._writer.write(full_command.encode())
        await self._writer.drain()
        
        # If it's a query command, wait for response
        if command.endswith("?"):
            return await self._wait_for_response(command, timeout)
            
        return None
        
    async def _wait_for_response(self, command: str, timeout: float) -> str:
        """Wait for a specific response."""
        response_event = asyncio.Event()
        response_data = None
        
        def response_handler(data: str):
            nonlocal response_data
            # Check if this is the response we're waiting for
            if data.startswith(RESPONSE_PREFIX + command.replace("?", "(")):
                response_data = data
                response_event.set()
                
        # Temporarily set response handler
        old_handler = self._response_handler
        self._response_handler = response_handler
        
        try:
            await asyncio.wait_for(response_event.wait(), timeout)
            return response_data
        except asyncio.TimeoutError:
            raise TimeoutError(f"No response to {command} within {timeout}s")
        finally:
            self._response_handler = old_handler
            
    async def _read_loop(self):
        """Continuously read responses from the device."""
        buffer = ""
        
        while self._connected:
            try:
                data = await self._reader.read(1024)
                if not data:
                    break
                    
                buffer += data.decode()
                
                # Process complete messages
                while COMMAND_TERMINATOR in buffer:
                    line, buffer = buffer.split(COMMAND_TERMINATOR, 1)
                    line = line.strip()
                    
                    if line:
                        logger.debug(f"Received: {line}")
                        
                        # Notify monitor if set
                        if self._monitor_callback:
                            self._monitor_callback("RX", line)
                        
                        # Handle based on prefix
                        if line.startswith(RESPONSE_PREFIX):
                            if self._response_handler:
                                self._response_handler(line)
                        elif line.startswith(ECHO_PREFIX):
                            # Command echo (feedback level 2)
                            pass
                            
            except Exception as e:
                logger.error(f"Read error: {e}")
                break
                
        self._connected = False
        
    def set_feedback_level(self, level: FeedbackLevel) -> None:
        """Set the feedback verbosity level."""
        self._feedback_level = level
        
    def set_monitor_callback(self, callback: Optional[Callable[[str, str], None]]) -> None:
        """
        Set a callback for monitoring all communication.
        
        Args:
            callback: Function that receives (direction, data) where
                     direction is "TX" or "RX" and data is the message
        """
        self._monitor_callback = callback
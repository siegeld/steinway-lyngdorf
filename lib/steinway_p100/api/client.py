"""HTTP API client for media information."""

import asyncio
import json
import logging
from typing import Optional, Dict, Any
from urllib.parse import quote

import aiohttp

from .models import MediaInfo, PlaybackState


logger = logging.getLogger(__name__)


class MediaApiClient:
    """Client for Steinway P100 HTTP API."""
    
    def __init__(self, host: str, port: int = 8080):
        """
        Initialize media API client.
        
        Args:
            host: Device hostname or IP
            port: API port (default: 8080)
        """
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self._session: Optional[aiohttp.ClientSession] = None
        self._api_available = True
        self._last_403_logged = False
        logger.info(f"MediaApiClient initialized with host={host}, port={port}, base_url={self.base_url}")
    
    async def __aenter__(self):
        """Async context manager entry."""
        self._session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._session:
            await self._session.close()
    
    async def _request(self, path: str, roles: str) -> Optional[Any]:
        """
        Make API request.
        
        Args:
            path: API path (e.g., "player:player/data")
            roles: Comma-separated roles to fetch
            
        Returns:
            Parsed JSON response or None
        """
        if not self._session:
            self._session = aiohttp.ClientSession()
        
        url = f"{self.base_url}/api/getData"
        params = {
            "path": path,
            "roles": roles
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Referer": f"http://{self.host}:{self.port}/",
            "Host": f"{self.host}:{self.port}"
        }
        
        logger.info(f"HTTP API Request: GET {url}")
        logger.info(f"Params: {params}")
        logger.info(f"Headers: {headers}")
        logger.info(f"Base URL: {self.base_url}")
        
        try:
            async with self._session.get(url, params=params, headers=headers, timeout=5) as response:
                if response.status == 200:
                    self._api_available = True
                    self._last_403_logged = False
                    return await response.json()
                elif response.status == 403:
                    self._api_available = False
                    if not self._last_403_logged:
                        response_text = await response.text()
                        logger.warning(f"HTTP API access forbidden (403). Media features will be disabled.")
                        logger.warning(f"Response status: {response.status}")
                        logger.warning(f"Response headers: {dict(response.headers)}")
                        logger.warning(f"Response body: {response_text[:500]}")  # First 500 chars
                        logger.warning(f"Request was to: {url}")
                        logger.warning(f"Using host: {self.host}:{self.port}")
                        self._last_403_logged = True
                    return None
                else:
                    logger.error(f"API request failed: {response.status}")
                    return None
        except asyncio.TimeoutError:
            logger.error("API request timed out")
            return None
        except Exception as e:
            logger.error(f"API request error: {e}")
            return None
    
    async def get_media_info(self) -> Optional[MediaInfo]:
        """
        Get current media information.
        
        Returns:
            MediaInfo object or None if no media playing or API unavailable
        """
        if not self._api_available:
            return None
        # Fetch player data
        data = await self._request(
            "player:player/data",
            "title,value,mediaData,icon,type"
        )
        
        if not data or len(data) < 2:
            return None
        
        # Parse the response
        player_data = data[1] if isinstance(data, list) and len(data) > 1 else {}
        
        if not isinstance(player_data, dict):
            return None
        
        # Extract basic info
        track_roles = player_data.get("trackRoles", {})
        media_data = track_roles.get("mediaData", {})
        meta_data = media_data.get("metaData", {})
        
        # Extract audio format info
        resources = media_data.get("resources", [])
        audio_info = resources[0] if resources else {}
        
        # Get playback state
        state_str = player_data.get("state", "unknown")
        try:
            state = PlaybackState(state_str)
        except ValueError:
            state = PlaybackState.UNKNOWN
        
        # Get timing info
        status = player_data.get("status", {})
        duration_ms = status.get("duration")
        
        # Get current position
        position_ms = await self._get_play_time()
        
        return MediaInfo(
            title=track_roles.get("title"),
            artist=meta_data.get("artist"),
            album=meta_data.get("album"),
            state=state,
            duration_ms=duration_ms,
            position_ms=position_ms,
            sample_rate=audio_info.get("sampleFrequency"),
            bit_depth=audio_info.get("bitsPerSample"),
            channels=audio_info.get("nrAudioChannels"),
            bit_rate=audio_info.get("bitRate"),
            service=meta_data.get("serviceID"),
            icon_url=track_roles.get("icon"),
            raw_data=player_data
        )
    
    async def _get_play_time(self) -> Optional[int]:
        """Get current playback position in milliseconds."""
        data = await self._request(
            "player:player/data/playTime",
            "value"
        )
        
        if data and isinstance(data, list) and len(data) > 0:
            time_data = data[0]
            if isinstance(time_data, dict) and "i64_" in time_data:
                return time_data["i64_"]
        
        return None
    
    async def _set_data(self, path: str, value: Dict[str, Any], roles: str = "activate") -> bool:
        """
        Send control command via setData API.
        
        Args:
            path: API path
            value: Value to set (will be JSON encoded)
            roles: Roles parameter (default: "activate")
            
        Returns:
            True if successful
        """
        if not self._session:
            self._session = aiohttp.ClientSession()
        
        url = f"{self.base_url}/api/setData"
        params = {
            "path": path,
            "roles": roles,
            "value": json.dumps(value)
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Referer": f"http://{self.host}:{self.port}/",
            "Host": f"{self.host}:{self.port}"
        }
        
        try:
            async with self._session.get(url, params=params, headers=headers, timeout=5) as response:
                if response.status == 200:
                    return True
                else:
                    logger.error(f"Control command failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"Control command error: {e}")
            return False
    
    async def play(self) -> bool:
        """Resume playback."""
        # The device uses "pause" as a toggle command
        return await self._set_data(
            "player:player/control",
            {"control": "pause"}
        )
    
    async def pause(self) -> bool:
        """Pause playback."""
        # The device uses "pause" as a toggle command
        return await self._set_data(
            "player:player/control",
            {"control": "pause"}
        )
    
    async def play_pause(self) -> bool:
        """Toggle play/pause."""
        # Just use the toggle command directly
        return await self._set_data(
            "player:player/control",
            {"control": "pause"}
        )
    
    async def next_track(self) -> bool:
        """Skip to next track."""
        return await self._set_data(
            "player:player/control",
            {"control": "next"}
        )
    
    async def previous_track(self) -> bool:
        """Skip to previous track."""
        return await self._set_data(
            "player:player/control",
            {"control": "previous"}
        )
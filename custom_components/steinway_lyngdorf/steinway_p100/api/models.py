"""Data models for media API."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any


class PlaybackState(Enum):
    """Playback states."""
    PLAYING = "playing"
    PAUSED = "paused"
    STOPPED = "stopped"
    UNKNOWN = "unknown"


@dataclass
class MediaInfo:
    """Media information from the HTTP API."""
    
    # Basic info
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    
    # Playback info
    state: PlaybackState = PlaybackState.UNKNOWN
    duration_ms: Optional[int] = None
    position_ms: Optional[int] = None
    
    # Audio format info
    sample_rate: Optional[int] = None
    bit_depth: Optional[int] = None
    channels: Optional[int] = None
    bit_rate: Optional[int] = None
    
    # Service info
    service: Optional[str] = None  # e.g., "roon", "spotify", "tidal"
    
    # Additional metadata
    icon_url: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None
    
    @property
    def is_playing(self) -> bool:
        """Check if media is currently playing."""
        return self.state == PlaybackState.PLAYING
    
    @property
    def progress_percent(self) -> Optional[float]:
        """Get playback progress as percentage."""
        if self.duration_ms and self.position_ms:
            return (self.position_ms / self.duration_ms) * 100
        return None
    
    @property
    def audio_format(self) -> str:
        """Get human-readable audio format string."""
        parts = []
        if self.sample_rate:
            parts.append(f"{self.sample_rate/1000:.1f}kHz")
        if self.bit_depth:
            parts.append(f"{self.bit_depth}bit")
        if self.channels:
            parts.append(f"{self.channels}ch")
        return " ".join(parts) if parts else "Unknown"
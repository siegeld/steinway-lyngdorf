"""Command builder for Steinway P100 protocol."""

from typing import Optional

from ..constants import Zone, FeedbackLevel


class CommandBuilder:
    """Build commands for Steinway P100 protocol."""
    
    @staticmethod
    def power_on(zone: Zone = Zone.MAIN) -> str:
        """Build power on command."""
        if zone == Zone.MAIN:
            return "POWERONMAIN"
        elif zone == Zone.ZONE2:
            return "POWERONZONE2"
        else:
            raise ValueError(f"Invalid zone: {zone}")
            
    @staticmethod
    def power_off(zone: Zone = Zone.MAIN) -> str:
        """Build power off command."""
        if zone == Zone.MAIN:
            return "POWEROFFMAIN"
        elif zone == Zone.ZONE2:
            return "POWEROFFZONE2"
        else:
            raise ValueError(f"Invalid zone: {zone}")
            
    @staticmethod
    def power_query(zone: Zone = Zone.MAIN) -> str:
        """Build power status query command."""
        if zone == Zone.MAIN:
            return "POWER?"
        elif zone == Zone.ZONE2:
            return "POWERZONE2?"
        else:
            raise ValueError(f"Invalid zone: {zone}")
            
    @staticmethod
    def volume_set(volume: float) -> str:
        """
        Build volume set command.
        
        Args:
            volume: Volume in dB (-99.9 to +24.0)
        """
        # Convert to protocol format (multiply by 10)
        vol_int = int(volume * 10)
        if vol_int < -999 or vol_int > 240:
            raise ValueError(f"Volume {volume} dB out of range")
        return f"VOL({vol_int})"
        
    @staticmethod
    def volume_up() -> str:
        """Build volume up command."""
        return "VOL+"
        
    @staticmethod
    def volume_down() -> str:
        """Build volume down command."""
        return "VOL-"
        
    @staticmethod
    def volume_query() -> str:
        """Build volume query command."""
        return "VOL?"
        
    @staticmethod
    def mute_on() -> str:
        """Build mute on command."""
        return "MUTEON"
        
    @staticmethod
    def mute_off() -> str:
        """Build mute off command."""
        return "MUTEOFF"
        
    @staticmethod
    def mute_toggle() -> str:
        """Build mute toggle command."""
        return "MUTE"
        
    @staticmethod
    def feedback_level(level: FeedbackLevel) -> str:
        """Build feedback level command."""
        return f"VERB({level.value})"
        
    @staticmethod
    def source_select(index: int) -> str:
        """Build source select command."""
        return f"SRC({index})"
        
    @staticmethod
    def source_query() -> str:
        """Build source query command."""
        return "SRC?"
        
    @staticmethod
    def zone2_volume_set(volume: float) -> str:
        """Build zone 2 volume set command."""
        vol_int = int(volume * 10)
        if vol_int < -999 or vol_int > 240:
            raise ValueError(f"Zone 2 volume {volume} dB out of range")
        return f"ZVOL({vol_int})"
        
    @staticmethod
    def zone2_volume_up(step: Optional[float] = None) -> str:
        """Build zone 2 volume up command."""
        if step is None:
            return "ZVOL+"
        else:
            step_int = int(step * 10)
            return f"ZVOL+({step_int})"
            
    @staticmethod
    def zone2_volume_down(step: Optional[float] = None) -> str:
        """Build zone 2 volume down command."""
        if step is None:
            return "ZVOL-"
        else:
            step_int = int(step * 10)
            return f"ZVOL-({step_int})"
            
    @staticmethod
    def volume_up(step: Optional[float] = None) -> str:
        """Build volume up command with optional step."""
        if step is None:
            return "VOL+"
        else:
            step_int = int(step * 10)
            return f"VOL+({step_int})"
            
    @staticmethod
    def volume_down(step: Optional[float] = None) -> str:
        """Build volume down command with optional step."""
        if step is None:
            return "VOL-"
        else:
            step_int = int(step * 10)
            return f"VOL-({step_int})"
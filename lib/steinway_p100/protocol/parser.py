"""Response parser for Steinway P100 protocol."""

import re
from typing import Dict, Any, Optional, Tuple, List, TYPE_CHECKING

from ..constants import RESPONSE_PREFIX, PowerState

if TYPE_CHECKING:
    from ..controls.source import Source


class ResponseParser:
    """Parse responses from Steinway P100."""
    
    @staticmethod
    def parse_power_status(response: str) -> PowerState:
        """
        Parse power status response.
        
        Response format: !POWER(0) or !POWER(1)
        """
        match = re.match(r"!POWER\((\d)\)", response)
        if match:
            return PowerState(int(match.group(1)))
        raise ValueError(f"Invalid power status response: {response}")
        
    @staticmethod
    def parse_zone2_power_status(response: str) -> PowerState:
        """
        Parse zone 2 power status response.
        
        Response format: !POWERZONE2(0) or !POWERZONE2(1)
        """
        match = re.match(r"!POWERZONE2\((\d)\)", response)
        if match:
            return PowerState(int(match.group(1)))
        raise ValueError(f"Invalid zone2 power status response: {response}")
        
    @staticmethod
    def parse_volume(response: str) -> float:
        """
        Parse volume response.
        
        Response format: !VOL(-550) to !VOL(240)
        Returns: Volume in dB (-55.0 to +24.0)
        """
        match = re.match(r"!VOL\((-?\d+)\)", response)
        if match:
            return int(match.group(1)) / 10.0
        raise ValueError(f"Invalid volume response: {response}")
        
    @staticmethod
    def parse_zone2_volume(response: str) -> float:
        """
        Parse zone 2 volume response.
        
        Response format: !ZVOL(-550) to !ZVOL(240)
        Returns: Volume in dB (-55.0 to +24.0)
        """
        match = re.match(r"!ZVOL\((-?\d+)\)", response)
        if match:
            return int(match.group(1)) / 10.0
        raise ValueError(f"Invalid zone2 volume response: {response}")
        
    @staticmethod
    def parse_mute(response: str) -> bool:
        """
        Parse mute status response.
        
        Response format: !MUTE(0) or !MUTE(1)
        Returns: True if muted, False otherwise
        """
        match = re.match(r"!MUTE\((\d)\)", response)
        if match:
            return match.group(1) == "1"
        raise ValueError(f"Invalid mute response: {response}")
        
    @staticmethod
    def parse_zone2_mute(response: str) -> bool:
        """
        Parse zone 2 mute status response.
        
        Response format: !ZMUTE(0) or !ZMUTE(1)
        Returns: True if muted, False otherwise
        """
        match = re.match(r"!ZMUTE\((\d)\)", response)
        if match:
            return match.group(1) == "1"
        raise ValueError(f"Invalid zone2 mute response: {response}")
        
    @staticmethod
    def parse_source(response: str) -> Tuple[int, str]:
        """
        Parse source response.
        
        Response format: !SRC(0)"DVD player"
        Returns: (index, name)
        """
        match = re.match(r'!SRC\((\d+)\)"([^"]+)"', response)
        if match:
            return int(match.group(1)), match.group(2)
        raise ValueError(f"Invalid source response: {response}")
        
    @staticmethod
    def parse_source_index(response: str) -> int:
        """
        Parse source index response.
        
        Response format: !SRC(0)
        Returns: source index
        """
        match = re.match(r"!SRC\((\d+)\)", response)
        if match:
            return int(match.group(1))
        raise ValueError(f"Invalid source index response: {response}")
        
    @staticmethod
    def parse_source_list(response: str) -> List["Source"]:
        """
        Parse source list response.
        
        Response format:
        !SRCCOUNT(4)
        !SRC(0)"DVD player"
        !SRC(1)"Blu-ray player"
        ...
        
        Returns: List of Source objects
        """
        from ..controls.source import Source
        
        lines = response.strip().split('\n')
        sources = []
        
        # First line should be source count
        count_match = re.match(r"!SRCCOUNT\((\d+)\)", lines[0])
        if not count_match:
            raise ValueError(f"Invalid source list response: missing SRCCOUNT")
            
        expected_count = int(count_match.group(1))
        
        # Parse each source
        for line in lines[1:]:
            match = re.match(r'!SRC\((\d+)\)"([^"]+)"', line)
            if match:
                index = int(match.group(1))
                name = match.group(2)
                sources.append(Source(index, name))
                
        if len(sources) != expected_count:
            raise ValueError(f"Expected {expected_count} sources, got {len(sources)}")
            
        return sources
        
    @staticmethod
    def parse_audio_mode_list(response: str) -> List["AudioMode"]:
        """
        Parse audio mode list response.
        
        Response format:
        !AUDMODECOUNT(8)
        !AUDMODE(0)"None"
        !AUDMODE(1)"dts Neo:X Cinema"
        ...
        
        Returns: List of AudioMode objects
        """
        from ..controls.audio_mode import AudioMode
        
        lines = response.strip().split('\n')
        modes = []
        
        # First line should be mode count
        count_match = re.match(r"!AUDMODECOUNT\((\d+)\)", lines[0])
        if not count_match:
            raise ValueError(f"Invalid audio mode list response: missing AUDMODECOUNT")
            
        expected_count = int(count_match.group(1))
        
        # Parse each mode
        for line in lines[1:]:
            match = re.match(r'!AUDMODE\((\d+)\)"([^"]+)"', line)
            if match:
                index = int(match.group(1))
                name = match.group(2)
                modes.append(AudioMode(index, name))
                
        if len(modes) != expected_count:
            raise ValueError(f"Expected {expected_count} modes, got {len(modes)}")
            
        return modes
        
    @staticmethod
    def parse_audio_mode(response: str) -> Tuple[int, str]:
        """
        Parse audio mode response.
        
        Response format: !AUDMODE(0)"None"
        Returns: (index, name)
        """
        match = re.match(r'!AUDMODE\((\d+)\)"([^"]+)"', response)
        if match:
            return int(match.group(1)), match.group(2)
        raise ValueError(f"Invalid audio mode response: {response}")
        
    @staticmethod
    def parse_audio_type(response: str) -> str:
        """
        Parse audio type response.
        
        Response format: !AUDTYPE"Dolby Atmos 7.1.4"
        Returns: Audio type string
        """
        match = re.match(r'!AUDTYPE"([^"]+)"', response)
        if match:
            return match.group(1)
        raise ValueError(f"Invalid audio type response: {response}")
        
    @staticmethod
    def parse_generic_response(response: str) -> Dict[str, Any]:
        """Parse any response into a generic dictionary."""
        response = response.strip()
        
        # Remove prefix
        if response.startswith(RESPONSE_PREFIX):
            response = response[1:]
            
        # Parse command(value)"string" format
        match = re.match(r'(\w+)\(([^)]*)\)(?:"([^"]*)")?', response)
        if match:
            command = match.group(1)
            value = match.group(2)
            string = match.group(3)
            
            return {
                "command": command,
                "value": value,
                "string": string
            }
            
        return {"raw": response}
"""Response parser for Steinway P100 protocol."""

import re
from typing import Dict, Any, Optional, Tuple

from ..constants import RESPONSE_PREFIX, PowerState


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
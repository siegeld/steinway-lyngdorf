#!/usr/bin/env python3
"""Example of volume control for Steinway P100."""

import asyncio
import logging
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from steinway_p100 import SteinwayP100Device


# Configure logging
logging.basicConfig(level=logging.INFO)


async def main():
    """Demonstrate volume control."""
    
    # Create device - replace with your IP address
    device = SteinwayP100Device.from_tcp("p100asp1")
    
    async with device:
        print("Volume Control Demo")
        print("==================")
        
        # Get current volume
        current_vol = await device.volume.get()
        is_muted = await device.volume.is_muted()
        print(f"Current volume: {current_vol:+.1f} dB")
        print(f"Muted: {is_muted}")
        
        # Set to a safe level
        print("\nSetting volume to -40 dB...")
        await device.volume.set(-40.0)
        
        # Volume up/down
        print("\nIncreasing volume by 2 dB...")
        await device.volume.up(2.0)
        new_vol = await device.volume.get()
        print(f"New volume: {new_vol:+.1f} dB")
        
        print("\nDecreasing volume by 5 dB...")
        await device.volume.down(5.0)
        new_vol = await device.volume.get()
        print(f"New volume: {new_vol:+.1f} dB")
        
        # Mute control
        print("\nMuting...")
        await device.volume.mute()
        is_muted = await device.volume.is_muted()
        print(f"Muted: {is_muted}")
        
        await asyncio.sleep(2)
        
        print("\nUnmuting...")
        await device.volume.unmute()
        is_muted = await device.volume.is_muted()
        print(f"Muted: {is_muted}")
        
        # Zone 2 volume
        print("\n\nZone 2 Volume")
        print("=============")
        z2_vol = await device.zone2_volume.get()
        print(f"Zone 2 volume: {z2_vol:+.1f} dB")
        
        # Volume limits
        min_vol, max_vol = await device.volume.get_limits()
        print(f"\nVolume range: {min_vol} to {max_vol} dB")


if __name__ == "__main__":
    asyncio.run(main())
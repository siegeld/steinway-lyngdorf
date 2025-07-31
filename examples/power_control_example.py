#!/usr/bin/env python3
"""Example of basic power control for Steinway P100."""

import asyncio
import logging
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from steinway_p100 import SteinwayP100Device, PowerState


# Configure logging
logging.basicConfig(level=logging.INFO)


async def main():
    """Demonstrate power control."""
    
    # Create device - replace with your IP address
    device = SteinwayP100Device.from_tcp("192.168.1.100")
    
    try:
        # Connect to device
        await device.connect()
        print("Connected to Steinway P100")
        
        # Get current power status
        status = await device.power.status()
        print(f"Current power state: {'ON' if status == PowerState.ON else 'OFF'}")
        
        # Turn on if off
        if status == PowerState.OFF:
            print("Turning on...")
            await device.power.on()
            await asyncio.sleep(2)  # Wait for device to power up
            
        # Check status again
        status = await device.power.status()
        print(f"Power state after turn on: {'ON' if status == PowerState.ON else 'OFF'}")
        
        # Turn off
        print("Turning off in 5 seconds...")
        await asyncio.sleep(5)
        await device.power.off()
        
        print("Device powered off")
        
    finally:
        # Always disconnect
        await device.disconnect()
        

# Alternative: Using context manager
async def context_manager_example():
    """Example using async context manager."""
    
    device = SteinwayP100Device.from_tcp("192.168.1.100")
    
    async with device:
        # Device is automatically connected
        status = await device.power.status()
        print(f"Power is {'ON' if status == PowerState.ON else 'OFF'}")
        
        # Toggle power
        await device.power.toggle()
        print("Power toggled")
        
    # Device is automatically disconnected


if __name__ == "__main__":
    asyncio.run(main())
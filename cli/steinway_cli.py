#!/usr/bin/env python3
"""CLI tool for testing Steinway P100 control."""

import asyncio
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

import click
from dotenv import load_dotenv
from steinway_p100 import SteinwayP100Device, PowerState, FeedbackLevel


# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)


# Configure logging based on environment
log_level = os.getenv('STEINWAY_LOG_LEVEL', 'INFO')
logging.basicConfig(
    level=getattr(logging, log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_env_default(key: str, default=None):
    """Get environment variable with STEINWAY_ prefix."""
    return os.getenv(f'STEINWAY_{key}', default)


@click.group()
@click.option('--host', '-h', 
              default=lambda: get_env_default('HOST'),
              help='IP address or hostname of Steinway P100 (env: STEINWAY_HOST)')
@click.option('--port', '-p', 
              default=lambda: int(get_env_default('PORT', '84')),
              help='TCP port (default: 84, env: STEINWAY_PORT)')
@click.option('--debug', is_flag=True, help='Enable debug logging')
@click.pass_context
def cli(ctx, host, port, debug):
    """Steinway P100 control CLI.
    
    Configuration can be provided via command line options or environment variables.
    Create a .env file in the project root with STEINWAY_HOST and STEINWAY_PORT.
    """
    if not host:
        click.echo("Error: No host specified. Use --host or set STEINWAY_HOST in .env file", err=True)
        ctx.exit(1)
        
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        
    # Show connection info in debug mode
    if debug:
        click.echo(f"Connecting to {host}:{port}")
        
    # Create device instance
    ctx.obj = SteinwayP100Device.from_tcp(host, port)


@cli.command()
@click.pass_obj
def on(device):
    """Turn on the main zone."""
    async def _on():
        async with device:
            await device.power.on()
            print("Main zone powered on")
            
    asyncio.run(_on())


@cli.command()
@click.pass_obj
def off(device):
    """Turn off the main zone."""
    async def _off():
        async with device:
            await device.power.off()
            print("Main zone powered off")
            
    asyncio.run(_off())


@cli.command()
@click.pass_obj
def toggle(device):
    """Toggle main zone power."""
    async def _toggle():
        async with device:
            await device.power.toggle()
            status = await device.power.status()
            print(f"Main zone is now {'ON' if status == PowerState.ON else 'OFF'}")
            
    asyncio.run(_toggle())


@cli.command()
@click.pass_obj
def status(device):
    """Get power status."""
    async def _status():
        async with device:
            main_status = await device.power.status()
            zone2_status = await device.zone2_power.status()
            
            print(f"Main zone: {'ON' if main_status == PowerState.ON else 'OFF'}")
            print(f"Zone 2: {'ON' if zone2_status == PowerState.ON else 'OFF'}")
            
    asyncio.run(_status())


@cli.group()
@click.pass_obj
def zone2(device):
    """Control Zone 2."""
    pass


@zone2.command('on')
@click.pass_obj
def zone2_on(device):
    """Turn on Zone 2."""
    async def _on():
        async with device:
            await device.zone2_power.on()
            print("Zone 2 powered on")
            
    asyncio.run(_on())


@zone2.command('off')
@click.pass_obj
def zone2_off(device):
    """Turn off Zone 2."""
    async def _off():
        async with device:
            await device.zone2_power.off()
            print("Zone 2 powered off")
            
    asyncio.run(_off())


@cli.group()
@click.pass_obj
def volume(device):
    """Control volume."""
    pass


@volume.command('get')
@click.pass_obj
def volume_get(device):
    """Get current volume."""
    async def _get():
        async with device:
            # Main zone
            vol = await device.volume.get()
            print(f"Main zone: {vol:+.1f} dB")
            
            # Zone 2
            z2_vol = await device.zone2_volume.get()
            print(f"Zone 2: {z2_vol:+.1f} dB")
            
    asyncio.run(_get())


@volume.command('set')
@click.argument('level', type=float)
@click.option('--zone2', is_flag=True, help='Set Zone 2 volume instead')
@click.pass_obj
def volume_set(device, level, zone2):
    """Set volume to specific level in dB."""
    async def _set():
        async with device:
            if zone2:
                await device.zone2_volume.set(level)
                print(f"Zone 2 volume set to {level:+.1f} dB")
            else:
                await device.volume.set(level)
                print(f"Main zone volume set to {level:+.1f} dB")
                
    asyncio.run(_set())


@volume.command('up')
@click.option('--step', default=0.5, help='Step size in dB')
@click.option('--zone2', is_flag=True, help='Control Zone 2 volume')
@click.pass_obj
def volume_up(device, step, zone2):
    """Increase volume."""
    async def _up():
        async with device:
            if zone2:
                await device.zone2_volume.up(step)
                new_vol = await device.zone2_volume.get()
                print(f"Zone 2 volume: {new_vol:+.1f} dB")
            else:
                await device.volume.up(step)
                new_vol = await device.volume.get()
                print(f"Main zone volume: {new_vol:+.1f} dB")
                
    asyncio.run(_up())


@volume.command('down')
@click.option('--step', default=0.5, help='Step size in dB')
@click.option('--zone2', is_flag=True, help='Control Zone 2 volume')
@click.pass_obj
def volume_down(device, step, zone2):
    """Decrease volume."""
    async def _down():
        async with device:
            if zone2:
                await device.zone2_volume.down(step)
                new_vol = await device.zone2_volume.get()
                print(f"Zone 2 volume: {new_vol:+.1f} dB")
            else:
                await device.volume.down(step)
                new_vol = await device.volume.get()
                print(f"Main zone volume: {new_vol:+.1f} dB")
                
    asyncio.run(_down())


@volume.command('mute')
@click.option('--zone2', is_flag=True, help='Mute Zone 2')
@click.pass_obj
def volume_mute(device, zone2):
    """Mute audio."""
    async def _mute():
        async with device:
            if zone2:
                await device.zone2_volume.mute()
                print("Zone 2 muted")
            else:
                await device.volume.mute()
                print("Main zone muted")
                
    asyncio.run(_mute())


@volume.command('unmute')
@click.option('--zone2', is_flag=True, help='Unmute Zone 2')
@click.pass_obj
def volume_unmute(device, zone2):
    """Unmute audio."""
    async def _unmute():
        async with device:
            if zone2:
                await device.zone2_volume.unmute()
                print("Zone 2 unmuted")
            else:
                await device.volume.unmute()
                print("Main zone unmuted")
                
    asyncio.run(_unmute())


@cli.group()
@click.pass_obj
def source(device):
    """Source selection commands."""
    pass


@source.command('list')
@click.pass_obj
def source_list(device):
    """List available sources."""
    async def _list():
        async with device:
            sources = await device.source.get_sources()
            current = await device.source.get_current()
            
            print("Available sources:")
            for src in sources:
                marker = " *" if src.index == current.index else ""
                print(f"  {src.index}: {src.name}{marker}")
                
    asyncio.run(_list())


@source.command('get')
@click.pass_obj
def source_get(device):
    """Show current source."""
    async def _get():
        async with device:
            current = await device.source.get_current()
            print(f"Current source: {current.index} - {current.name}")
            
    asyncio.run(_get())


@source.command('set')
@click.argument('source', required=True)
@click.pass_obj
def source_set(device, source):
    """Select a source by index or name."""
    async def _set():
        async with device:
            # Try as index first
            try:
                index = int(source)
                await device.source.select(index)
                current = await device.source.get_current()
                print(f"Selected source: {current.index} - {current.name}")
            except ValueError:
                # Try as name
                await device.source.select_by_name(source)
                current = await device.source.get_current()
                print(f"Selected source: {current.index} - {current.name}")
                
    asyncio.run(_set())


@source.command('next')
@click.pass_obj
def source_next(device):
    """Select next source."""
    async def _next():
        async with device:
            await device.source.next()
            current = await device.source.get_current()
            print(f"Selected source: {current.index} - {current.name}")
            
    asyncio.run(_next())


@source.command('prev')
@click.pass_obj
def source_prev(device):
    """Select previous source."""
    async def _prev():
        async with device:
            await device.source.previous()
            current = await device.source.get_current()
            print(f"Selected source: {current.index} - {current.name}")
            
    asyncio.run(_prev())


@cli.group()
@click.pass_obj
def audio(device):
    """Audio mode and processing commands."""
    pass


@audio.command('modes')
@click.pass_obj
def audio_modes(device):
    """List available audio processing modes."""
    async def _modes():
        async with device:
            modes = await device.audio_mode.get_modes()
            current = await device.audio_mode.get_current()
            
            print("Available audio modes:")
            for mode in modes:
                marker = " *" if mode.index == current.index else ""
                print(f"  {mode.index}: {mode.name}{marker}")
                
    asyncio.run(_modes())


@audio.command('get')
@click.pass_obj
def audio_get(device):
    """Show current audio mode."""
    async def _get():
        async with device:
            current = await device.audio_mode.get_current()
            print(f"Current audio mode: {current.index} - {current.name}")
            
    asyncio.run(_get())


@audio.command('set')
@click.argument('mode', required=True)
@click.pass_obj
def audio_set(device, mode):
    """Select an audio mode by index or name."""
    async def _set():
        async with device:
            # Try as index first
            try:
                index = int(mode)
                await device.audio_mode.select(index)
                current = await device.audio_mode.get_current()
                print(f"Selected audio mode: {current.index} - {current.name}")
            except ValueError:
                # Try as name
                await device.audio_mode.select_by_name(mode)
                current = await device.audio_mode.get_current()
                print(f"Selected audio mode: {current.index} - {current.name}")
                
    asyncio.run(_set())


@audio.command('next')
@click.pass_obj
def audio_next(device):
    """Select next audio mode."""
    async def _next():
        async with device:
            await device.audio_mode.next()
            current = await device.audio_mode.get_current()
            print(f"Selected audio mode: {current.index} - {current.name}")
            
    asyncio.run(_next())


@audio.command('prev')
@click.pass_obj
def audio_prev(device):
    """Select previous audio mode."""
    async def _prev():
        async with device:
            await device.audio_mode.previous()
            current = await device.audio_mode.get_current()
            print(f"Selected audio mode: {current.index} - {current.name}")
            
    asyncio.run(_prev())


@audio.command('type')
@click.pass_obj
def audio_type(device):
    """Show current audio input type."""
    async def _type():
        async with device:
            audio_type = await device.audio_mode.get_audio_type()
            print(f"Audio input type: {audio_type}")
            
    asyncio.run(_type())


@cli.group()
@click.pass_obj
def media(device):
    """Media playback information and control."""
    pass


@media.command('info')
@click.pass_obj
def media_info(device):
    """Show current media information."""
    async def _info():
        if not device.media:
            print("Media API not available (no host configured)")
            return
            
        async with device.media:
            info = await device.media.get_media_info()
            
            if not info:
                print("No media playing")
                return
            
            # Display media info
            print("Now Playing:")
            if info.title:
                print(f"  Title: {info.title}")
            if info.artist:
                print(f"  Artist: {info.artist}")
            if info.album:
                print(f"  Album: {info.album}")
            if info.service:
                print(f"  Service: {info.service}")
            
            # Playback info
            print(f"\nPlayback: {info.state.value}")
            if info.position_ms and info.duration_ms:
                pos_sec = info.position_ms // 1000
                dur_sec = info.duration_ms // 1000
                pos_min, pos_sec = divmod(pos_sec, 60)
                dur_min, dur_sec = divmod(dur_sec, 60)
                print(f"  Position: {pos_min}:{pos_sec:02d} / {dur_min}:{dur_sec:02d}")
                if info.progress_percent:
                    print(f"  Progress: {info.progress_percent:.1f}%")
            
            # Audio format
            if info.audio_format != "Unknown":
                print(f"\nAudio Format: {info.audio_format}")
                if info.bit_rate:
                    print(f"  Bit Rate: {info.bit_rate:,} bps")
            
    asyncio.run(_info())


@media.command('play')
@click.pass_obj
def media_play(device):
    """Resume playback."""
    async def _play():
        if not device.media:
            print("Media API not available (no host configured)")
            return
            
        async with device.media:
            if await device.media.play():
                print("Playback resumed")
            else:
                print("Failed to resume playback")
                
    asyncio.run(_play())


@media.command('pause')
@click.pass_obj
def media_pause(device):
    """Pause playback."""
    async def _pause():
        if not device.media:
            print("Media API not available (no host configured)")
            return
            
        async with device.media:
            if await device.media.pause():
                print("Playback paused")
            else:
                print("Failed to pause playback")
                
    asyncio.run(_pause())


@media.command('toggle')
@click.pass_obj
def media_toggle(device):
    """Toggle play/pause."""
    async def _toggle():
        if not device.media:
            print("Media API not available (no host configured)")
            return
            
        async with device.media:
            if await device.media.play_pause():
                info = await device.media.get_media_info()
                if info:
                    print(f"Playback {info.state.value}")
            else:
                print("Failed to toggle playback")
                
    asyncio.run(_toggle())


@media.command('next')
@click.pass_obj
def media_next(device):
    """Skip to next track."""
    async def _next():
        if not device.media:
            print("Media API not available (no host configured)")
            return
            
        async with device.media:
            if await device.media.next_track():
                print("Skipped to next track")
            else:
                print("Failed to skip track")
                
    asyncio.run(_next())


@media.command('prev')
@click.pass_obj
def media_prev(device):
    """Skip to previous track."""
    async def _prev():
        if not device.media:
            print("Media API not available (no host configured)")
            return
            
        async with device.media:
            if await device.media.previous_track():
                print("Skipped to previous track")
            else:
                print("Failed to skip track")
                
    asyncio.run(_prev())


@cli.command()
@click.pass_obj
@click.option('--duration', '-d', default=0, help='Monitor duration in seconds (0=forever)')
@click.option('--feedback', '-f', 
              type=click.Choice(['0', '1', '2'], case_sensitive=False),
              default='1',
              help='Feedback level: 0=minimal, 1=status, 2=echo')
def monitor(device, duration, feedback):
    """Monitor all communication with the device in real-time."""
    
    # Colors for terminal output
    TX_COLOR = '\033[32m'  # Green
    RX_COLOR = '\033[34m'  # Blue
    INFO_COLOR = '\033[33m'  # Yellow
    RESET_COLOR = '\033[0m'
    
    def monitor_callback(direction: str, data: str):
        """Callback to display monitored data."""
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        
        if direction == "TX":
            color = TX_COLOR
            symbol = "→"
        else:
            color = RX_COLOR
            symbol = "←"
            
        print(f"{timestamp} {color}{symbol} {data}{RESET_COLOR}")
    
    async def _monitor():
        # Set monitor callback
        device._connection.set_monitor_callback(monitor_callback)
        
        try:
            async with device:
                # Set feedback level
                fb_level = FeedbackLevel(int(feedback))
                await device.set_feedback_level(fb_level)
                
                print(f"{INFO_COLOR}Monitoring Steinway P100 communication...{RESET_COLOR}")
                print(f"{INFO_COLOR}Feedback level: {fb_level.name}{RESET_COLOR}")
                print(f"{INFO_COLOR}Press Ctrl+C to stop{RESET_COLOR}")
                print(f"{INFO_COLOR}{'='*60}{RESET_COLOR}")
                
                # Keep monitoring
                if duration > 0:
                    await asyncio.sleep(duration)
                else:
                    # Run forever until interrupted
                    while True:
                        await asyncio.sleep(1)
                        
        except KeyboardInterrupt:
            print(f"\n{INFO_COLOR}Monitoring stopped{RESET_COLOR}")
    
    try:
        asyncio.run(_monitor())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    cli()
# Steinway Lyngdorf Integration

This integration provides control of Steinway Lyngdorf P100/P200/P300 surround sound processors via Home Assistant.

## Features

### Media Player Entity
- **Power control**: Turn on/off main zone
- **Volume control**: Set volume, volume up/down, mute/unmute
- **Source selection**: Select from available inputs
- **Attributes**: Current audio mode, available audio modes, audio format info

### Custom Services
- **steinway_lyngdorf.set_audio_mode**: Select audio processing mode (Dolby, DTS, Auro-3D, etc.)
- **steinway_lyngdorf.set_room_perfect**: Select RoomPerfect focus position (coming soon)
- **steinway_lyngdorf.set_lipsync**: Adjust audio/video sync delay (coming soon)

## Configuration

The integration is configured via the UI. You'll need:
- **Host**: IP address or hostname of your Steinway Lyngdorf processor
- **Port**: TCP port (default: 84)

## Requirements
- Steinway Lyngdorf P100, P200, or P300 processor
- Network connection to the processor
- Processor must have IP control enabled

## Installation via HACS

1. Add this repository to HACS as a custom repository
2. Search for "Steinway Lyngdorf" in HACS
3. Install the integration
4. Restart Home Assistant
5. Add the integration via Settings → Devices & Services → Add Integration

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/siegeld/steinway-p100/issues).
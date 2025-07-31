# Claude Development Guide

This document contains information for Claude (or other AI assistants) to understand the project structure and development practices.

## Project Overview

This is a Python library and Home Assistant integration for controlling Steinway & Sons P100/P200/P300 surround sound processors. The project includes:
- Python library with async/await support
- Command-line interface (CLI) for testing
- Home Assistant custom component (media_player entity)
- Support for both TCP/IP and RS232 serial connections
- HACS compatibility

## Key Design Decisions

1. **Async First**: All communication is asynchronous using Python's asyncio
2. **Type Hints**: Full type annotations throughout the codebase
3. **Environment Variables**: Configuration via .env file for development
4. **Virtual Environment**: Using venv for dependency isolation
5. **HACS Compatible**: Structure supports Home Assistant HACS installation
6. **Coordinator Pattern**: Home Assistant uses DataUpdateCoordinator for efficiency
7. **Auto-reconnection**: Connection failures are handled gracefully

## Current Implementation Status

### Completed
- Power control (main zone and Zone 2)
- Volume control with mute
- Source selection
- Audio mode control (Dolby, DTS, etc.)
- CLI tool with all features
- Home Assistant media_player entity
- Custom services for advanced features
- Connection management with auto-reconnect
- HTTP API client for media information
- Media playback controls (play/pause/next/previous)
- Media metadata display in Home Assistant

### To-Do
- RoomPerfect position control
- Lipsync adjustment
- Unit tests
- Serial connection support
- Multiview control (P200/P300)

## Development Workflow

### Making Changes
1. Always use the virtual environment
2. Run tests before committing
3. Use type hints for all new code
4. Follow existing code patterns
5. Update CHANGELOG.md

### Testing Commands
```bash
make test          # Run tests
make lint          # Check code style
make format        # Auto-format code
make run-cli ARGS="on"  # Test CLI commands
```

### Version Management
```bash
./commit.sh        # Automated commit workflow
```
This script:
- Cleans build artifacts
- Updates CHANGELOG.md
- Bumps version
- Creates commit and tag

## Code Style

- Use Black for formatting (line length 88)
- Follow PEP 8 with type hints (PEP 484)
- Docstrings for all public methods
- Async methods prefixed with `async_` in Home Assistant code
- Use logging instead of print statements

## Common Tasks

### Adding a New Command
1. Add to `protocol/builder.py`
2. Add parser to `protocol/parser.py` if needed
3. Add to appropriate control class
4. Add CLI command
5. Update Home Assistant if applicable
6. Update tests

### Adding a New Control Feature
1. Create control class in `controls/`
2. Add to device.py
3. Export in `controls/__init__.py`
4. Add CLI commands
5. Update media_player.py if needed

### Debugging Connection Issues
1. Use monitor mode: `./run_cli.sh monitor`
2. Enable debug logging: `--debug` flag
3. Check response timeouts in `connection/base.py`
4. Monitor Home Assistant logs

## Important Files

### Library Core
- `lib/steinway_p100/constants.py` - Protocol constants
- `lib/steinway_p100/device.py` - Main device class
- `lib/steinway_p100/protocol/` - Command building/parsing
- `lib/steinway_p100/controls/` - Feature-specific controls

### CLI
- `cli/steinway_cli.py` - CLI implementation
- `run_cli.sh` - Convenience wrapper

### Home Assistant
- `custom_components/steinway_lyngdorf/` - HA integration
- `coordinator.py` - Connection management
- `media_player.py` - Entity implementation
- `services.yaml` - Service definitions

### Configuration
- `.env` - Local configuration (not in git)
- `hacs.json` - HACS metadata
- `manifest.json` - Integration metadata

## Protocol Notes

- Commands start with `!` and end with `\r`
- Responses start with `!` (status) or `#` (echo)
- Feedback levels: 0=minimal, 1=status, 2=echo
- Some commands timeout (e.g., MUTE?)
- Volume is in 0.1dB units (multiply by 10)

## Home Assistant Notes

- Uses coordinator pattern for updates
- Updates every 10 seconds when powered on
- Automatic reconnection with exponential backoff
- Volume mapped from 0-1 to -60dB to 0dB
- Custom services for features not in media_player
- Attributes show audio mode and format
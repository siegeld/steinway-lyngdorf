# Steinway P100 Control Library

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange)](https://hacs.xyz)

Python library and Home Assistant integration for controlling Steinway & Sons P100/P200/P300 surround sound processors.

## Features

- 🔌 **Multiple Connection Types**: TCP/IP and RS232 serial support
- 🏠 **Home Assistant Integration**: Full HACS-compatible custom component
- 🎛️ **Comprehensive Control**: Power, volume, sources, audio modes, and more
- 🔄 **Async/Await**: Modern Python async implementation
- 📡 **Real-time Updates**: Automatic status updates with configurable feedback levels
- 🎭 **Multi-zone**: Control main zone and Zone 2 independently
- 🎵 **Media Information**: Track metadata, playback state, and audio format via HTTP API
- ⏯️ **Media Control**: Play, pause, next, and previous track commands

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/siegeld/steinway-p100.git
cd steinway-p100

# Option 1: Quick install (recommended)
make install

# Option 2: Install with development tools
make install-dev

# Option 3: Manual install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configuration

The CLI uses environment variables for default configuration. Set up your `.env` file:

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your device's hostname or IP
nano .env  # or use your preferred editor
```

Configuration options in `.env`:
```bash
STEINWAY_HOST=p100asp1        # Device hostname or IP address (required)
STEINWAY_PORT=84              # TCP port (default: 84)
STEINWAY_LOG_LEVEL=INFO       # Logging: DEBUG, INFO, WARNING, ERROR
```

### 3. Running the CLI

**Easy method** - Use the convenience script (no venv activation needed):
```bash
./run_cli.sh on          # Turn on main zone
./run_cli.sh off         # Turn off main zone
./run_cli.sh status      # Get power status
./run_cli.sh monitor     # Monitor communication
```

**Manual method** - Activate virtual environment first:
```bash
# Activate virtual environment
source venv/bin/activate

# Run commands
python cli/steinway_cli.py on
python cli/steinway_cli.py off
python cli/steinway_cli.py status

# Zone 2 control
python cli/steinway_cli.py zone2 on    # Turn on Zone 2
python cli/steinway_cli.py zone2 off   # Turn off Zone 2

# Override host from command line
python cli/steinway_cli.py --host 192.168.1.100 on

# Enable debug logging
python cli/steinway_cli.py --debug status

# Using make (automatically uses venv)
make run-cli ARGS="on"
make run-cli ARGS="status"

# Monitor mode - see all communication in real-time
python cli/steinway_cli.py monitor                    # Monitor forever
python cli/steinway_cli.py monitor --duration 30      # Monitor for 30 seconds
python cli/steinway_cli.py monitor --feedback 2       # Show command echoes too

# Media playback control (requires HTTP API on port 8080)
python cli/steinway_cli.py media info                 # Show current track info
python cli/steinway_cli.py media play                 # Resume playback
python cli/steinway_cli.py media pause                # Pause playback
python cli/steinway_cli.py media next                 # Skip to next track
python cli/steinway_cli.py media prev                 # Skip to previous track
```

**Monitor Mode**: The `monitor` command shows all communication between the CLI and the device in real-time:
- Green arrows (→) show commands sent to the device
- Blue arrows (←) show responses from the device
- Use `--feedback` to control verbosity (0=minimal, 1=status updates, 2=echo all commands)

**Note**: The CLI will use the host from `.env` by default. You can override it with `--host` option.

### 4. Python Library Usage

```python
import asyncio
from steinway_p100 import SteinwayP100Device, PowerState

async def main():
    # Connect using TCP
    device = SteinwayP100Device.from_tcp("p100asp1")
    
    async with device:
        # Power control
        await device.power.on()
        status = await device.power.status()
        print(f"Power: {'ON' if status == PowerState.ON else 'OFF'}")
        
        # Future: Volume control
        # await device.volume.set(-30.0)  # -30dB
        # await device.volume.mute()
        
        # Future: Source selection
        # await device.source.select("Blu-ray")

asyncio.run(main())
```

## Installation

### As a Python Library

```bash
pip install steinway-p100
```

### Home Assistant (via HACS)

1. Add this repository to HACS as a custom repository
2. Search for "Steinway Lyngdorf" in HACS
3. Install the integration
4. Restart Home Assistant
5. Add integration via Settings → Devices & Services → Add Integration → Steinway Lyngdorf

#### Home Assistant Features

- **Media Player Entity**
  - Power on/off
  - Volume control with mute
  - Source selection
  - Audio mode in attributes
  - Media playback controls (play, pause, next, previous)
  - Now playing information (title, artist, album)
  - Media position and duration
  - Audio format details in attributes
  
- **Custom Services**
  - `steinway_lyngdorf.set_audio_mode` - Select Dolby, DTS, Auro-3D modes
  - `steinway_lyngdorf.set_room_perfect` - Select RoomPerfect positions (coming soon)
  - `steinway_lyngdorf.set_lipsync` - Adjust audio/video sync (coming soon)

## Supported Models

- Steinway & Sons P100
- Steinway & Sons P200
- Steinway & Sons P300
- Head Unit

## Documentation

- [API Reference](docs/api.md) - Detailed API documentation
- [Protocol Guide](docs/protocol.md) - Communication protocol details
- [Home Assistant Setup](docs/homeassistant.md) - HA integration guide
- [Examples](examples/) - Usage examples

## Development

### Project Structure

```
steinway-p100/
├── lib/                      # Python library
│   └── steinway_p100/
├── custom_components/        # Home Assistant integration
│   └── steinway_lyngdorf/
├── cli/                      # Command-line tool
├── tests/                    # Test suite
└── examples/                 # Usage examples
```

### Makefile Commands

```bash
make help        # Show all available commands
make install     # Create venv and install package
make install-dev # Install with development dependencies
make test        # Run test suite
make lint        # Run code linters (ruff, mypy)
make format      # Format code with black
make clean       # Remove venv and build artifacts
make run-cli ARGS="on"  # Run CLI commands
```

### Running Tests

```bash
make test
# or
./venv/bin/pytest tests/
```

### Code Quality

```bash
make lint    # Check code style and types
make format  # Auto-format code
```

## Troubleshooting

### Common Issues

1. **"No host specified" error**
   - Make sure `.env` file exists and contains `STEINWAY_HOST=your-device-ip`
   - Or provide host via command line: `python cli/steinway_cli.py --host p100.local on`

2. **Connection timeout**
   - Verify the device is on the network and reachable
   - Check if port 84 is correct (default for P100)
   - Try using IP address instead of hostname

3. **Import errors**
   - Make sure virtual environment is activated: `source venv/bin/activate`
   - Reinstall dependencies: `pip install -r requirements.txt`

4. **"python: command not found"**
   - Use `python3` instead of `python`
   - Make sure Python 3.8+ is installed

### Verify Installation

```bash
# Check Python version
python3 --version  # Should be 3.8 or higher

# Test import (with venv activated)
python3 -c "import steinway_p100; print(steinway_p100.__version__)"

# Test CLI help
./run_cli.sh --help

# Quick connectivity test
./run_cli.sh status
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Steinway & Sons for the excellent P100/P200/P300 processors
- The Home Assistant community
- Contributors and testers
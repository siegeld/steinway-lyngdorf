# Claude Development Notes

## Project Overview
This project implements a Python library for controlling Steinway P100 surround sound processors, with plans for Home Assistant integration via HACS.

## Architecture Decisions

### 1. Async-First Design
- All communication is async using `asyncio`
- Enables non-blocking operations for Home Assistant integration
- Supports both TCP and Serial connections

### 2. Library Structure
```
lib/steinway_p100/
├── connection/      # Abstract connection layer
├── protocol/        # Command building and response parsing
├── controls/        # Feature-specific control classes
└── device.py        # High-level API
```

### 3. Protocol Implementation
- Text-based protocol: commands start with `!` and end with `\r`
- Three feedback levels: minimal (0), status updates (1), echo+status (2)
- Response parsing using regex for flexibility

### 4. Development Setup
- Using Python venv for isolation
- pyproject.toml for modern Python packaging
- Environment variables via .env for configuration
- Makefile for common tasks

## Key Design Patterns

### Connection Abstraction
```python
class BaseConnection(ABC):
    async def connect() -> None
    async def send_command(command: str) -> Optional[str]
    async def disconnect() -> None
```

### Control Classes
Each feature (power, volume, etc.) gets its own control class:
```python
class PowerControl:
    async def on() -> None
    async def off() -> None
    async def status() -> PowerState
```

### High-Level API
```python
async with SteinwayP100Device.from_tcp("p100.local") as device:
    await device.power.on()
    await device.volume.set(-30.0)
```

## Implementation Status

### Completed
- ✅ Core connection layer (TCP/Serial)
- ✅ Protocol parser and builder
- ✅ Power control (main zone and zone 2)
- ✅ CLI tool with .env support
- ✅ Basic project structure

### TODO
- [ ] Volume control
- [ ] Source selection
- [ ] Audio modes and processing
- [ ] RoomPerfect settings
- [ ] Lipsync adjustment
- [ ] Home Assistant custom component
- [ ] HACS configuration
- [ ] Comprehensive tests
- [ ] CI/CD pipeline

## Testing Strategy
1. Unit tests for protocol parsing
2. Mock connection tests for controls
3. Integration tests with real device
4. Home Assistant component tests

## Future Enhancements
- Auto-discovery via Bonjour
- WebSocket support for real-time updates
- Multi-device support
- Scene management
- Backup/restore settings
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure and architecture
- Core connection layer with TCP and Serial support
- Protocol parser and command builder
- Power control for main zone and Zone 2
- CLI tool with environment variable support
- Development setup with virtual environment
- Project documentation (README, CLAUDE, CHANGELOG)
- Modern Python packaging with pyproject.toml
- Makefile for common development tasks

### Changed
- Nothing yet

### Deprecated
- Nothing yet

### Removed
- Nothing yet

### Fixed
- Nothing yet

### Security
- Nothing yet

## [0.1.0] - 2024-XX-XX (Planned)

### Planned Features
- Volume control with mute functionality
- Source selection and management
- Audio mode selection (Dolby, DTS, etc.)
- RoomPerfect position and voicing control
- Lipsync adjustment
- Basic Home Assistant integration
- HACS compatibility

## Roadmap

### Version 0.2.0
- Multiview control (P200/P300)
- Speaker configuration management
- Advanced audio settings
- Zone 2 full control

### Version 0.3.0
- Auto-discovery via Bonjour
- WebSocket support for real-time updates
- Home Assistant UI enhancements
- Scene management

### Version 1.0.0
- Full protocol implementation
- Comprehensive test coverage
- Production-ready Home Assistant component
- Complete documentation

[Unreleased]: https://github.com/yourusername/steinway-p100/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/steinway-p100/releases/tag/v0.1.0
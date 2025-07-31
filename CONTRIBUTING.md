# Contributing to Steinway P100 Control Library

Thank you for your interest in contributing to the Steinway P100 Control Library! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to be respectful and constructive in all interactions.

## How to Contribute

### Reporting Issues

1. Check if the issue already exists
2. Include device model (P100/P200/P300)
3. Provide detailed steps to reproduce
4. Include relevant logs (with sensitive data removed)
5. Mention your Python version and OS

### Suggesting Features

1. Check the roadmap in CHANGELOG.md
2. Open a discussion issue first
3. Describe the use case clearly
4. Consider protocol limitations

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add/update tests as needed
5. Run tests and linters (`make test lint`)
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/steinway-p100.git
cd steinway-p100

# Setup development environment
./setup-dev.sh

# Activate virtual environment
source venv/bin/activate

# Run tests
make test

# Run linters
make lint

# Format code
make format
```

## Coding Standards

### Python Style
- Follow PEP 8
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use Black for formatting
- Use Ruff for linting

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Reference issues when applicable

### Documentation
- Update docstrings for new functions/classes
- Update README.md for new features
- Add examples for complex features

## Testing

### Unit Tests
- Test individual components in isolation
- Mock external dependencies
- Aim for high coverage

### Integration Tests
- Test with real device when possible
- Document device-specific behaviors
- Handle timeout scenarios

### Example Test
```python
async def test_power_on():
    device = SteinwayP100Device.from_tcp("test.local")
    with patch.object(device._connection, 'send_command') as mock:
        await device.power.on()
        mock.assert_called_with("POWERONMAIN")
```

## Protocol Implementation

When implementing new protocol features:

1. Study the protocol documentation
2. Test with real device
3. Handle all response types
4. Document any quirks or limitations
5. Update protocol guide if needed

## Home Assistant Integration

For HA component changes:

1. Follow HA development guidelines
2. Test with latest HA version
3. Update manifest.json version
4. Test HACS installation

## Questions?

Feel free to open an issue for:
- Clarification on protocol behavior
- Architecture decisions
- Implementation approaches

Thank you for contributing!
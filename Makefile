.PHONY: help venv install install-dev clean test lint format run-cli sync-hacs

# Default target
help:
	@echo "Available commands:"
	@echo "  make venv        - Create a Python virtual environment"
	@echo "  make install     - Install the package and dependencies"
	@echo "  make install-dev - Install with development dependencies"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linters (ruff, mypy)"
	@echo "  make format      - Format code with black"
	@echo "  make clean       - Remove build artifacts and cache"
	@echo "  make run-cli     - Run the CLI (requires ARGS='command')"
	@echo "  make sync-hacs   - Sync library to custom component for HACS"

# Create virtual environment
venv:
	python3 -m venv venv
	@echo "Virtual environment created. Activate with:"
	@echo "  source venv/bin/activate"

# Install package and dependencies
install: venv sync-hacs
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -e ./lib

# Install with development dependencies
install-dev: venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -e "./lib[dev]"

# Run tests
test:
	./venv/bin/pytest tests/

# Run linters
lint:
	./venv/bin/ruff check lib/
	./venv/bin/mypy lib/

# Format code
format:
	./venv/bin/black lib/
	./venv/bin/ruff check --fix lib/

# Clean up
clean:
	rm -rf venv/
	rm -rf lib/build/
	rm -rf lib/*.egg-info/
	rm -rf custom_components/steinway_lyngdorf/steinway_p100
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run CLI tool
run-cli:
	./venv/bin/python cli/steinway_cli.py $(ARGS)

# Sync library to custom component for HACS
sync-hacs:
	@echo "Syncing library to custom component..."
	rm -rf custom_components/steinway_lyngdorf/steinway_p100
	cp -r lib/steinway_p100 custom_components/steinway_lyngdorf/
	find custom_components/steinway_lyngdorf/steinway_p100 -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "Library synced to custom component"
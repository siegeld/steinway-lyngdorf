.PHONY: help venv install install-dev clean test lint format run-cli

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

# Create virtual environment
venv:
	python3 -m venv venv
	@echo "Virtual environment created. Activate with:"
	@echo "  source venv/bin/activate"

# Install package and dependencies
install: venv
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
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run CLI tool
run-cli:
	./venv/bin/python cli/steinway_cli.py $(ARGS)
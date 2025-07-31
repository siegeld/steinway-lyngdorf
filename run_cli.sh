#!/bin/bash
# Convenience script to run the Steinway P100 CLI with virtual environment

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Setting up..."
    make install
fi

# Run the CLI with all arguments passed through
exec ./venv/bin/python cli/steinway_cli.py "$@"
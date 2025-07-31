#!/bin/bash
# Quick setup script for development

echo "Setting up Steinway P100 development environment..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install package with dev dependencies
echo "Installing package and dependencies..."
pip install -e "./lib[dev]"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To test the CLI:"
echo "  python cli/steinway_cli.py --help"
echo "  python cli/steinway_cli.py on"
echo ""
echo "Environment variables are loaded from .env file"
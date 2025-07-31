"""Setup configuration for steinway-p100."""

from pathlib import Path
from setuptools import setup, find_packages

# Read version from VERSION file
version_file = Path(__file__).parent.parent / "VERSION"
version = version_file.read_text().strip() if version_file.exists() else "0.1.0"

setup(
    name="steinway-p100",
    version=version,
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pyserial-asyncio>=0.6",
        "click>=8.0",
        "python-dotenv>=0.19",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21",
            "pytest-cov>=4.0",
            "black>=23.0",
            "ruff>=0.1.0",
            "mypy>=1.0",
            "pip-tools>=7.0",
        ]
    },
)
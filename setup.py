#!/usr/bin/env python
"""
Setup script for BugBountyKE-KSP API Client
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="bugbounty-ksp-api-client",
    version="1.0.1",
    author="BugBountyKE-KSP Team -- Theoriest",
    author_email="mawiralee02@gmail.com",
    description="Official Python SDK for BugBountyKE-KSP platform API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BugBounty-MockingBird/bugbounty-ksp-api-client",
    project_urls={
        "Bug Tracker": "https://github.com/BugBounty-MockingBird/bugbounty-ksp-api-client/issues",
        "Documentation": "https://bugbounty-mockingbird.github.io/Documentation/python-sdk/",
        "Source Code": "https://github.com/BugBounty-MockingBird/bugbounty-ksp-api-client",
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    include_package_data=True,
)

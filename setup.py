"""Setup script for awesome-selfhosted-alternatives CLI tool."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="selfhosted-cli",
    version="1.0.0",
    author="aayushmanrajputdev",
    author_email="aayush@rajput.dev",
    description="CLI tool for self-hosted alternatives catalog",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aayushmanrajputdev/awesome-selfhosted-alternatives",
    packages=find_packages(where="cli"),
    package_dir={"": "cli"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "tabulate>=0.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "selfhosted=cli.selfhosted_cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/aayushmanrajputdev/awesome-selfhosted-alternatives/issues",
        "Source": "https://github.com/aayushmanrajputdev/awesome-selfhosted-alternatives",
        "Documentation": "https://github.com/aayushmanrajputdev/awesome-selfhosted-alternatives#readme",
    },
)
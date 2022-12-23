"""Package configuration."""
from setuptools import find_packages, setup

setup(
    name="debian_package_stats",
    version="0.1",
    packages=find_packages(where="pkg_stats"),
    package_dir={"": "pkg_stats"},
    install_requires=[],
    ## Entry point for command line and function to be executed
    entry_points={
        'console_scripts': ['pkg-stats=cli:main'],
    }
)
from setuptools import setup, find_packages

setup(
    name="openrgb-flowers-blooming",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "numpy>=1.20.0",
        "openrgb-python>=0.3.5",
        "hidapi>=0.14.0",
        "pystray>=0.19.5",
        "pillow>=10.0.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0.0"],
    },
    entry_points={
        "console_scripts": [
            "openrgb-flowers=openrgb_flowers.cli.main:main",
        ],
    },
)

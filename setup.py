
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="onebite",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "argparse",
    ],
    entry_points={
        "console_scripts": [
            "onebite=onebite.__main__:main",
        ],
    },
)

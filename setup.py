#!/usr/bin/env python

from setuptools import setup

setup(
    name="fijio",
    version="0.1.0.dev0",
    description="Python package for writing imageJ format tif file",
    author="Stephane Rigaud",
    author_email="stephane.rigaud@pasteur.fr",
    url="https://github.com/StRigaud/fijio",
    packages=["fijio"],
    install_requires=[
        "tifffile",
        "numpy",
        "matplotlib",
    ],
)

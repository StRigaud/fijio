#!/usr/bin/env python

from setuptools import setup

setup(
    name="fijio",
    version="0.1.0.dev0",
    description="Python package for writing imageJ format tif file",
    long_description="Python package for writing imageJ format tif file",
    long_description_content_type="text/markdown",
    author="Stephane Rigaud",
    author_email="stephane.rigaud@pasteur.fr",
    url="https://github.com/StRigaud/fijio",
    packages=["fijio"],
    install_requires=[
        "tifffile",
        "numpy",
        "matplotlib",
    ],
    tests_require=[
        "pytest",
        "pytest-cov",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: BSD License",
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    project_urls={
        "Documentation": "https://github.com/StRigaud/fijio#README.md",
        "Source": "https://github.com/StRigaud/fijio/",
        "Issues": "https://github.com/StRigaud/fijio/issues",
    },
)

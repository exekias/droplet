#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from nazs import __version__

setup(
    name="NAZS",
    version=__version__,
    author="NAZS Team",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=[
        "bin/manage.py"
    ],
)

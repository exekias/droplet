#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages
from droplet import __version__


def relpath(filename):
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.relpath(os.path.join(here, filename))

setup(
    name='droplet',
    version=__version__,
    url='https://github.com/exekias/droplet',
    author='droplet team',
    license='AGPLv3',
    description='',
    long_description=open(relpath('README.md')).read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=[
        relpath('bin/droplet'),
    ],
    install_requires=open(relpath('requirements.txt')).readlines(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
    ],
    entry_points={
        'droplet.app': [
            'network=droplet.network',
            'samba=droplet.samba',
        ],
    },
)

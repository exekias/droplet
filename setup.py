#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from nazs import __version__

setup(
    name='nazs',
    version=__version__,
    url='https://github.com/exekias/nazs',
    author='NAZS team',
    license='AGPLv3',
    description='',
    long_description=open('README.md').read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=[
        'bin/nazs'
    ],
    install_requires=open('requirements.txt').readlines(),
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
        'nazs.app': [
            'network=nazs.network',
            'samba=nazs.samba',
        ],
    },
)

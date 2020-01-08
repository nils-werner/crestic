#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='crestic',
    version='0.1',
    description='Configurable restic',
    author='Nils Werner',
    author_email='nils.werner@gmail.com',
    packages=['crestic'],
    entry_points={
        'console_scripts': [
            'crestic = crestic:main',
        ]
    },
)

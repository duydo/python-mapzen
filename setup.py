#!/usr/bin/env python
from setuptools import setup

__author__ = 'duydo'

setup(
    name='mapzen',
    version='0.1',
    description='Python Client for Mapzen APIs',
    license='ALv2',
    author='Duy Do',
    author_email='doquocduy@gmail.com',
    url='https://github.com/duydo/python-mapzen',
    packages=['mapzen'],
    install_requires=['six'],
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5"
    ]
)

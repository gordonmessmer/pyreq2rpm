#!/usr/bin/env python3

from setuptools import setup

setup(
    name='pyreq2rpm',
    version='0.0.1',
    description='Convert Python requirements to rpm',
    license='MIT',
    packages=['pyreq2rpm'],
    install_requires=['setuptools'],
    setup_requires=['setuptools'],
    tests_require=['pytest'],
)

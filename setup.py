#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name="mantra",
    version="0.1.0",
    packages=["mantra"],
    install_requires=[
        "cython",
        "ujson",
        "colorlog",
        "uvloop",
        "aiohttp",
        "dataset",
        "thrift",
        "pycrypto",
        "multidict",
        "requests",
    ],
)

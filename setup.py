#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-yamltree',
    version='0.1.2',
    author='Semyon Maryasin',
    author_email='simeon@maryasin.name',
    maintainer='Semyon Maryasin',
    maintainer_email='simeon@maryasin.name',
    license='MIT',
    url='https://github.com/MarSoft/pytest-yamltree',
    description='Create or check file/directory trees described by YAML',
    long_description=read('README.rst'),
    py_modules=['pytest_yamltree'],
    install_requires=['pytest>=3.1.1', 'pyyaml'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'yamltree = pytest_yamltree',
        ],
    },
)

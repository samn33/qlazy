# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

VERSION = '0.0.15'

try:
    with open('README.md') as f:
        README = f.read()
except IOError:
    README = ''

setup(
    name='qlazypy',
    version=VERSION,
    url='https://github.com/samn33/qlazy',
    author='Sam.N',
    author_email='saminriver33@gmail.com',
    description='quantum computer application framework',
    long_description=README,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    license='Apace License 2.0',
    classifiers={
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'License :: OSI Approved :: Apache License 2.0',
    },
    keywords=['quantum','gate', 'framework'],
    entry_points="""
    [console_scripts]
    qlazypy = qlazypy:main
    """,
)

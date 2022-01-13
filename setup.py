# -*- coding: utf-8 -*-
import os
import pathlib
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext as build_ext_orig

_VERSION = '0.2.3'

class CMakeExtension(Extension):

    def __init__(self, name):
        super().__init__(name, sources=[])

class build_ext(build_ext_orig):

    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        cwd = pathlib.Path().absolute()
        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        extdir = pathlib.Path(self.get_ext_fullpath(ext.name))
        extdir.mkdir(parents=True, exist_ok=True)
        config = 'Debug' if self.debug else 'Release'
        cmake_args = [
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + str(extdir.parent.parent.absolute()),
            '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY=' + str(extdir.parent.parent.parent.absolute()),
            '-DCMAKE_BUILD_TYPE=' + config
        ]
        build_args = [
            '--config', config,
            '--', '-j4'
        ]
        os.chdir(str(build_temp))
        self.spawn(['cmake', str(cwd)] + cmake_args)
        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'] + build_args)
        os.chdir(str(cwd))

setup(
    name='qlazy',
    version=_VERSION,
    url='https://github.com/samn33/qlazy',
    author='Sam.N',
    author_email='saminriver33@gmail.com',
    description='Quantum Computing Simulator',
    long_description='',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy'
    ],
    license='Apache Software License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'License :: OSI Approved :: Apache Software License',
    ],
    keywords=['quantum', 'simulator'],
    ext_modules=[CMakeExtension('qlazy/lib/c/qlz')],
    cmdclass={
        'build_ext': build_ext,
    },
    entry_points="""
    [console_scripts]
    qlazy = qlazy.core:main
    """,
)

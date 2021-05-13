import re

from setuptools import setup, find_packages
from os import path

HERE = path.abspath(path.dirname(__file__))


def readfile(*parts):
    with open(path.join(HERE, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = readfile(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string')


setup(
    name='calculatorLobachevsky',
    version=find_version('calculatorLobachevsky', '__init__.py'),
    description='Implementation of a calculator for a project for Nizhny Novgorod'
                ' State University named after N.I. Lobachevsky',
    url='https://github.com/Kishkin-Vlad/calculatorLobachevsky',
    author='Vladislav Kishkin',
    author_email='vladkishkin1@yandex.ru',
    license='Proprietary License',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.7.5',
        'Operating System :: POSIX :: Linux'
    ],
    packages=find_packages(where='.', include=('calculatorLobachevsky*',)),
    package_dir={'calculatorLobachevsky': 'calculatorLobachevsky'},
    python_requires='>=3.7'
)

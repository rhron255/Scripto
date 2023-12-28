import pathlib
import os

from setuptools import setup, find_packages

PROJECT_VERSION = os.getenv('SCRIPTO_VERSION')

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='Scripto',
    version=PROJECT_VERSION,
    description='A simple framework to help you build scripts faster!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ron Hasleton',
    author_email='ronhasleton@gmail.com',
    keywords='scripting, auto, cli, argparse',
    package_dir={'': 'src'},
    packages=find_packages(where='src', include=['*']),
    python_requires='>=3.7, <4',
    license='GNU GPLv3'
)

split_version = list(map(lambda x: int(x), PROJECT_VERSION.split('.')))
split_version[-1] = split_version[-1] + 1
os.putenv('SCRIPTO_VERSION', '.'.join(split_version))

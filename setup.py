from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='AutoScript',
    version='0.0.1',
    description='A simple framework to help you build scripts faster!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ron Hasleton',
    author_email='ronhasleton@gmail.com',
    keywords='scripting, auto, cli, argparse',
    package_dir={'': 'AutoScript'},
    packages=find_packages(where='AutoScript'),
    python_requires='>=3.7, <4',
    license='GNU GPLv3'
)
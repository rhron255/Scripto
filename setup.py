import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='Scripto',
    version='0.0.6',
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

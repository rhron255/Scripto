# Scripto
[![Build Project](https://github.com/rhron255/Scripto/actions/workflows/python-build.yaml/badge.svg)](https://github.com/rhron255/Scripto/actions/workflows/python-build.yaml)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![python: version](https://img.shields.io/pypi/pyversions/scripto.svg)](https://img.shields.io/pypi/pyversions/scripto.svg?color=%2334D058)

Are you sick of writing long and annoying argparse initialization code?
Worry no more - the future is here!

Scripto is a Python package designed to transform your scripts into a powerful CLI tool using decorators.
As in the example below, you can use the `@script.register()` decorator on your main business logic functions
to effortlessly generate a feature-rich command-line interface.

## Features

- Seamless integration with argparse.
- Simple and intuitive syntax inspired by Flask.
- Automatically generates CLI commands from decorated functions.
- Ideal for turning scripts into organized and user-friendly command-line tools.

## Usage

1. Install Scripto.
   You can install Scripto using pip:
    ```bash
    pip install scripto
    ```

2. Decorate your main business logic functions with `@script.register()`.
3. Run your script to enjoy the generated CLI:

    ```python
    from scripto.app import Scripto
    
    script = Scripto('script')
    
    @script.register()
    def my_command(arg1, arg2):
        """
        Description of your command.
        """
        # Your business logic here
    
    if __name__ == "__main__":
        script.run()
    ```

## Complex Examples

See the [example](exmaples) scripts provided.

## About the rationale

We all like the simple automations, and nifty little scripts play a vital role in the life of every developer.

Many times, what was a simple 3 line script turned into a slightly larger one,
and then all of your friends want to use it too.

Which is when you find out, your user interface sucks.

This framework aims to simplify the creation of the command line interface of such scripts.
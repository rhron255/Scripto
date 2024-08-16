"""
An example script with two modes of operation:
`jsonify.py prettify path\to\file.json` will re-indent your file.
`jsonify.py minify path\to\file.json` will un-indent your file.

Try running the script yourself to see the help message generated!
"""
import json

from scripto.app import Scripto

script = Scripto('JSONify', enable_interactive_mode=True)


@script.register()
def prettify(path: str, indent: int = 4):
    """
    Reads a JSON file, and re-indents it.
    :param path: The path to the file.
    :param indent: How many spaces to use when indenting.
    :return: None
    """
    data = []
    with open(path, 'r') as file:
        data = json.load(file)
    with open(path, 'w') as file:
        json.dump(data, file, indent=indent)


@script.register()
def minify(path: str):
    """
    Reads a JSON file, and un-indents it.
    :param path: The path to the file.
    :return: None
    """
    data = []
    with open(path, 'r') as file:
        data = json.load(file)
    with open(path, 'w') as file:
        json.dump(data, file)


if __name__ == '__main__':
    script.run()

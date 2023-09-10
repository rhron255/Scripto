import pathlib
import re
import sys

import rich
from pyfiglet import figlet_format


def split_to_dict(string: str):
    """
    Splits a string into a dict from a var=val format, works with single and double quotes.
    :param string: The string to read into a dict.
    :return: A dictionary containing the set values
    """
    search_string = f'{string} '
    pattern = re.compile('(\w+)=(?P<quote>["\']*)([^"\']+)(?P=quote)\s+')
    results = [match[::2] for match in pattern.findall(search_string)]
    return dict(results)


def print_intro(description: str, script_name=pathlib.Path(sys.argv[0]).name[:-3], color='white'):
    """
    Prints an introduction to the script, mainly meant for interactive shells.
    :param description: The description of the script.
    :param script_name: The name of script, by default is taken from the name of the file.
    :param color: Colors the title in the provided color name. See rich package for color options.
    :return:
    """
    rich.print(f'[{color}]{figlet_format(script_name, font="slant")}[/{color}]')
    print(description)

import inspect
import re
import warnings
from types import FunctionType
from typing import List, Dict


def get_description(func: FunctionType) -> str:
    """
    Returns the description part of the documentation of the function.
    :param func: The function to retrieve documentation from.
    :return: The documentation of the function.
    """
    docstring = inspect.getdoc(func)
    doc_end = docstring.find(':')
    if doc_end == -1:
        return docstring
    return docstring[:doc_end].strip()


def get_parameters(func: FunctionType) -> List[Dict]:
    """
    Yields the parameters of the function given.
    For each parameter, returns a dictionary with 'name', 'type' and 'description'.
    :param func: The function to yield parameters for.
    :return: A dictionary with data regarding the parameter.
    """
    signature = inspect.signature(func)
    docstring = inspect.getdoc(func)
    for param in signature.parameters.values():
        result = re.compile(f':param {param.name}:\s*(?P<desc>.*)\s*:param').search(
            docstring.replace('\n', ''))
        if result is None:
            result = re.compile(f':param {param.name}:\s*(?P<desc>.*)\s*:return').search(
                docstring.replace('\n', ''))
        parameter = {
            'name': param.name,
            'type': param.annotation,
            'description': result.groupdict()['desc'] if result is not None else ''
        }
        if param.default is not inspect.Parameter.empty:
            parameter['default'] = param.default
        yield parameter


def make_kebab_case(string: str) -> str:
    """
    Converts a string to kebab case, great for CLI arguments.
    :param string: The string to convert.
    :return: A kebab case formatted string
    """
    return string.lower().replace(' ', '-').replace('_', '-')


def get_first_doc_sentence(func):
    description = get_description(func)
    return description.split('.')[0] if '.' in description else description


def validate_parameters_in_docstring(func: FunctionType, supress_warnings=False):
    signature = inspect.signature(func)
    docstring = inspect.getdoc(func)
    for param in signature.parameters.values():
        result = re.compile(f':param {param.name}:\s*(?P<desc>.*)\s*:param').search(
            docstring.replace('\n', ''))
        if result is None:
            result = re.compile(f':param {param.name}:\s*(?P<desc>.*)\s*:return').search(
                docstring.replace('\n', ''))
            if result is None and not supress_warnings:
                warnings.warn(
                    f'Documentation not sufficient to parse description for parameter: "{param.name}" in function: "{func.__name__}".',
                    stacklevel=3)
        if param.annotation is inspect.Parameter.empty:
            return TypeError(
                f'No type annotation found for parameter: "{param.name}" in function: "{func.__name__}".')


def get_argument_names(func: FunctionType) -> List[str]:
    return [key for key in inspect.signature(func).parameters.keys()]

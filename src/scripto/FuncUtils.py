#pylint: disable=W1401
"""
A utility module for various function parsing functions.
"""
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
    doc_end = docstring.find('\n:')
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
    parameters = []
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
        parameters.append(parameter)
    return parameters


def make_kebab_case(string: str) -> str:
    """
    Converts a string to kebab case, great for CLI arguments.
    :param string: The string to convert.
    :return: A kebab case formatted string
    """
    return string.lower().replace(' ', '-').replace('_', '-')


def get_first_doc_sentence(func) -> str:
    """
    Returns the first sentence of the documentation.
    :param func: The function to retrieve the documentation from.
    :return: The first sentence of the documentation.
    """
    description = get_description(func)
    return description.split('.')[0] if '.' in description else description


def validate_parameters_in_docstring(func: FunctionType, supress_warnings=False) -> None:
    """
    Validates that all parameters in the function signature have type annotations (imperative to core functionality).
    Also, raises warnings if the documentation cannot be parsed into an appropriate description.
    :param func: The function to validate.
    :param supress_warnings: Whether to supress the generated warnings.
    :return: None
    """
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
            raise TypeError(
                f'No type annotation found for parameter: "{param.name}" in function: "{func.__name__}".')


def get_argument_names(func: FunctionType) -> List[str]:
    """
    Retrieves all argument names from a function's signature.
    :param func: The function to parse.
    :return: A list of argument names.
    """
    return list(inspect.signature(func).parameters.keys())

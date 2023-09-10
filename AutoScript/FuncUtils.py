import inspect
import json
import re
import warnings
from types import FunctionType
from typing import List, Dict

import pydantic
from pydantic import BaseModel


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
    """
    Returns the first sentence of a function's documentation.
    :param func:
    :return:
    """
    description = get_description(func)
    return description.split('.')[0] if '.' in description else description


def validate_parameters_in_docstring(func: FunctionType, supress_warnings=False):
    """
    Validates that the parameters present in a function's signature are actually present in its docstring.
    Also, ensures that all the parameters in the signature have a type annotation.
    :param func: The function to validate.
    :param supress_warnings: Whether to silence user warnings about lack of annotations.
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
            return TypeError(
                f'No type annotation found for parameter: "{param.name}" in function: "{func.__name__}".')


def get_argument_names(func: FunctionType) -> List[str]:
    """
    Returns the names of arguments that a function takes.
    :param func: The function to retrieve argument names from.
    :return: The names of arguments the function takes.
    """
    return [key for key in inspect.signature(func).parameters.keys()]


def strip_dict_to_func_args(func: FunctionType, args: dict) -> dict:
    """
    Strips a dict to arguments of the function supplied.
    :param func: The function to strip the dict according to.
    :param args: The args dict that needs stripping.
    :return: The stripped dict.
    """
    new_args = {}
    for k in args.keys():
        if k in get_argument_names(func):
            new_args[k] = args[k]
    return new_args


def create_model(func: FunctionType) -> BaseModel:
    """
    Creates a pydantic BaseModel matching the function's signature.
    :param func: The function to create the model for.
    :return: The base model representing the functions parameters.
    """
    arg_tuple_dict = {}
    arg: inspect.Parameter
    for arg in inspect.signature(func).parameters.values():
        arg_tuple_dict[arg.name] = (arg.annotation, arg.default)
    return pydantic.create_model(f'{func.__name__.title()}Model', **arg_tuple_dict)


def parse_dict_to_parameters(func: FunctionType, args: dict):
    """
    Takes a dict and parses the data within according to the types of the function's parameters.
    :param func: The function to parse the arguments for.
    :param args: The arguments to parse.
    :return: A dict of parsed arguments for the function's signature.
    """
    model = create_model(func)
    data = model.model_validate_json(json.dumps(args)).model_dump(exclude_unset=True)
    return {arg for arg in data.items() if arg[1] is not inspect.Parameter.empty}

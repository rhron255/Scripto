import inspect
import re
from types import FunctionType


def get_description(func: FunctionType):
    """
    Returns the description part of the documentation of the function.
    :param func: The function to retrieve documentation from.
    :return: The documentation of the function.
    """
    docstring = inspect.getdoc(func)
    doc_end = docstring.find(':')
    if doc_end == -1:
        return docstring
    return docstring[:doc_end]


def get_parameters(func: FunctionType):
    """
    Yields the parameters of the function given.
    For each parameter, returns a dictionary with 'name', 'type' and 'description'.
    :param func: The function to yield parameters for.
    :return: A dictionary with data regarding the parameter.
    """
    signature = inspect.signature(func)
    docstring = inspect.getdoc(func)
    for param in signature.parameters.values():
        print(param)
        result = re.compile(f':param {param.name}:\s*(?P<desc>.*)\s*:param').search(
            docstring.replace('\n', ''))
        if result is None:
            result = re.compile(f':param {param.name}:\s*(?P<desc>.*)\s*:return').search(
                docstring.replace('\n', ''))
            if result is None:
                raise ValueError(
                    f'Documentation not sufficient to parse description for parameter: "{param.name}" in function: "{func.__name__}".')
        if param.annotation is inspect.Parameter.empty:
            raise TypeError(f'No type annotation found for parameter: "{param.name}" in function: "{func.__name__}".')
        yield {'name': param.name, 'type': param.annotation, 'description': result.groupdict()['desc']}

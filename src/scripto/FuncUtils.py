# pylint: disable=W1401
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
    docstring = get_escaped_docstring(func)
    if docstring is not None:
        doc_end = docstring.find("\n:")
        if doc_end == -1:
            return docstring
        return docstring[:doc_end].strip()


def get_escaped_docstring(func):
    doc = inspect.getdoc(func)
    if doc:
        return doc.replace("%", "%%")
    return None


def get_parameters(func: FunctionType) -> List[Dict]:
    """
    Yields the parameters of the function given.
    For each parameter, returns a dictionary with 'name', 'type' and 'description'.
    :param func: The function to yield parameters for.
    :return: A dictionary with data regarding the parameter.
    """
    signature = inspect.signature(func)
    docstring = get_escaped_docstring(func)
    parameters = []
    for param in signature.parameters.values():
        result = None
        if docstring:
            # Update regex to handle multi-line parameter descriptions
            result = re.search(
                rf":param {param.name}:\s*(?P<desc>.*?)(?=\n\s*:\w|\Z)",
                # Stops at the next directive or end-of-docstring
                docstring,
                flags=re.DOTALL,
            )
        parameter = {
            "name": param.name,
            "type": (
                param.annotation if param.annotation != inspect.Parameter.empty else str
            ),
            "description": result.group("desc").strip() if result is not None else "",
        }
        if param.default is not inspect.Parameter.empty:
            parameter["default"] = param.default
        parameters.append(parameter)
    return parameters


def make_kebab_case(string: str) -> str:
    """
    Converts a string to kebab case, great for CLI arguments.
    :param string: The string to convert.
    :return: A kebab case formatted string
    """
    return string.lower().replace(" ", "-").replace("_", "-")


def get_first_doc_sentence(func) -> str | None:
    """
    Returns the first sentence of the documentation.
    :param func: The function to retrieve the documentation from.
    :return: The first sentence of the documentation.
    """
    description = get_description(func)
    if description:
        return description.split(".")[0] if "." in description else description
    return None


def validate_parameters_in_docstring(
    func: FunctionType, suppress_warnings=False
) -> None:
    """
    Validates that all parameters in the function signature have type annotations (imperative to core functionality).
    Also, raises warnings if the documentation cannot be parsed into an appropriate description.
    :param func: The function to validate.
    :param suppress_warnings: Whether to suppress the generated warnings.
    :return: None
    """
    signature = inspect.signature(func)
    docstring = get_escaped_docstring(func)

    for param in signature.parameters.values():
        if docstring:
            # Updated regex to correctly handle multi-line descriptions and stop at the next directive
            result = re.search(
                rf":param {param.name}:\s*(?P<desc>.*?)(?=\n\s*:\w|\Z)",
                # Stops at the next directive or end of docstring
                docstring,
                flags=re.DOTALL,
            )
            if result is None and not suppress_warnings:
                warnings.warn(
                    f'Documentation not sufficient to parse description for parameter: "{param.name}" in function: "{func.__name__}".',
                    stacklevel=3,
                )
        if param.annotation is inspect.Parameter.empty and not suppress_warnings:
            warnings.warn(
                f'No type annotations for: "{param.name}" in function: "{func.__name__}", may result in unexpected behaviour.',
                stacklevel=3,
            )


def get_argument_names(func: FunctionType) -> List[str]:
    """
    Retrieves all argument names from a function's signature.
    :param func: The function to parse.
    :return: A list of argument names.
    """
    return list(inspect.signature(func).parameters.keys())

import argparse
import functools
from types import FunctionType
from typing import List

from FuncUtils import generate_parser, generate_parser_definitions, generate_action_settings, \
    validate_parameters_in_docstring


class AutoCli:
    _description: str
    _functions: List[FunctionType] = []

    def __init__(self, description):
        self._description = description

    def run(self):
        if len(self._functions) == 0:
            raise ValueError('No functions registered...')
        elif len(self._functions) == 1:
            function = self._functions[0]
            function(**vars(generate_parser(function).parse_args()))
        else:
            parent_parser = argparse.ArgumentParser(description=self._description)
            sub = parent_parser.add_subparsers(required=True)
            for func in self._functions:
                name, settings = generate_parser_definitions(func)
                sub_parser = sub.add_parser(name, **settings)
                for name, settings in generate_action_settings(func):
                    sub_parser.add_argument(name, **settings)
            args = parent_parser.parse_args()
            args.func(args)

    def auto_cli(self, *config_args, **config_kwargs):
        def registration_function(func: FunctionType):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            parameter_validation_exception = validate_parameters_in_docstring(func)
            if parameter_validation_exception is not None:
                raise parameter_validation_exception
            self._functions.append(func)
            return wrapper

        return registration_function

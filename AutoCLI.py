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
            parent_parser = argparse.ArgumentParser(description=self._description, conflict_handler='resolve')
            sub = parent_parser.add_subparsers(required=True)
            for func in self._functions:
                name, settings = generate_parser_definitions(func)
                sub_parser = sub.add_parser(name, **settings, conflict_handler='resolve')
                for name, settings in generate_action_settings(func):
                    if type(name) is list:
                        sub_parser.add_argument(*name, **settings)
                    else:
                        sub_parser.add_argument(name, **settings)
                sub_parser.set_defaults(func=func)
            # Parsing the arguments passed to the program.
            args = parent_parser.parse_args()
            # Popping the function used out of the arguments passed to the function.
            func_args = {**vars(args)}
            func_args.pop('func')
            args.func(**func_args)

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

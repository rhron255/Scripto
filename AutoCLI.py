import argparse
import functools
from argparse import ArgumentParser
from types import FunctionType
from typing import List, Tuple

from FuncUtils import generate_parser, make_kebab_case, get_description, generate_parser_definitions, \
    generate_action_settings


# def auto_cli(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         arg_parser = generate_parser(func)
#         return func(**vars(arg_parser.parse_args()))
#
#     return wrapper

def auto_cli(*config_args, **config_kwargs):
    def registration_function(func: FunctionType):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        AutoCli.register_func(func)
        return wrapper

    return registration_function


class AutoCli:
    _description: str
    _functions: List[FunctionType] = []
    _instance = None

    def __init__(self, description):
        self._description = description
        if AutoCli._instance is None:
            AutoCli._instance = self

    def register_function(self, func: FunctionType):
        self._functions.append(func)

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

    @classmethod
    def register_func(cls, func: FunctionType):
        AutoCli._instance.register_function(func)

import argparse
import functools
from argparse import ArgumentParser
from types import FunctionType
from typing import List, Tuple

from FuncUtils import generate_parser, make_kebab_case


def auto_cli(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        arg_parser = generate_parser(func)
        return func(**vars(arg_parser.parse_args()))

    return wrapper


class AutoCli:
    _description: str
    _sub_parsers: List[Tuple[FunctionType, ArgumentParser]] = []

    def __init__(self, description):
        self._description = description

    def register_function(self, func: FunctionType):
        self._sub_parsers.append((func, generate_parser(func)))

    def run(self):
        if len(self._sub_parsers) == 0:
            raise ValueError('No functions registered...')
        elif len(self._sub_parsers) == 1:
            function, parser = self._sub_parsers[0]
            function(**vars(parser.parse_args()))
        else:
            parent_parser = argparse.ArgumentParser(description=self._description)
            sub = parent_parser.add_subparsers(required=True)
            for func, inner_parser in self._sub_parsers:
                inner_parser.set_defaults(func=func)
                sub.add_parser(name=make_kebab_case(func.__name__), parents=[inner_parser], add_help=False)
            args = parent_parser.parse_args()
            args.func(args)

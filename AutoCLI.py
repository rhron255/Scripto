import argparse
import functools
import logging
from types import FunctionType
from typing import List

from FuncUtils import generate_action_settings, validate_parameters_in_docstring


def add_logging_flags(parser):
    log_level = parser.add_mutually_exclusive_group()
    log_level.add_argument('--trace', dest='log_level', action='store_const', const='trace',
                           help='Set log level to trace')
    log_level.add_argument('--debug', dest='log_level', action='store_const', const='debug',
                           help='Set log level to debug')
    log_level.add_argument('--warn', dest='log_level', action='store_const', const='warn',
                           help='Set log level to warning')
    log_level.add_argument('--info', dest='log_level', action='store_const', const='info',
                           help='Set log level to info')


class AutoCli:
    _description: str
    _silence: bool
    _functions: List[FunctionType] = []
    _use_logger = False

    def __init__(self, description, suppress_warnings=False, auto_log=False):
        self._description = description
        self._silence = suppress_warnings
        self._use_logger = auto_log

    def run(self):
        parser = argparse.ArgumentParser(description=self._description, conflict_handler='resolve')
        if len(self._functions) == 0:
            raise ValueError('No functions registered...')
        elif len(self._functions) == 1:
            function = self._functions[0]
            self.add_function_to_parser(function, parser)
        else:
            sub = parser.add_subparsers(required=True)
            for func in self._functions:
                name, settings = generate_parser_definitions(func)
                sub_parser = sub.add_parser(name, **settings, conflict_handler='resolve')
                self.add_function_to_parser(func, sub_parser)

        # Parsing the arguments passed to the program.
        args = parser.parse_args()
        # Popping the function used out of the arguments passed to the function.
        func_args = {**vars(args)}
        func_args.pop('func')
        if self._use_logger:
            logging.basicConfig(level=func_args['log_level'])
            func_args.pop('log_level')
        args.func(**func_args)

    def add_function_to_parser(self, func, parser):
        for name, settings in generate_action_settings(func):
            if type(name) is list:
                parser.add_argument(*name, **settings)
            else:
                parser.add_argument(name, **settings)
        if self._use_logger:
            add_logging_flags(parser)
        parser.set_defaults(func=func)

    def auto_cli(self, *config_args, **config_kwargs):
        def registration_function(func: FunctionType):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            parameter_validation_exception = validate_parameters_in_docstring(func, self._silence)
            if parameter_validation_exception is not None:
                raise parameter_validation_exception
            self._functions.append(func)
            return wrapper

        return registration_function

import argparse
import functools
import logging
from types import FunctionType
from typing import List

from Scripto.FuncUtils import generate_action_settings, validate_parameters_in_docstring, generate_parser_definitions, \
    get_argument_names, make_kebab_case


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


class Scripto:
    _description: str
    _silence: bool
    _functions: List[FunctionType] = []
    _arg_initializers = {}
    _use_logger = False

    def __init__(self, description, suppress_warnings=False, auto_log=False):
        self._description = description
        self._silence = suppress_warnings
        self._use_logger = auto_log

    def run(self):
        parser = argparse.ArgumentParser(description=self._description, conflict_handler='resolve',
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        if len(self._functions) == 0:
            raise ValueError('No functions registered...')
        if len(self._functions) == 1:
            function = self._functions[0]
            self.add_function_to_parser(function, parser)
        else:
            sub = parser.add_subparsers(required=True)
            for func in self._functions:
                name, settings = generate_parser_definitions(func)
                sub_parser = sub.add_parser(name, **settings, conflict_handler='resolve',
                                            formatter_class=argparse.RawDescriptionHelpFormatter)
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
            target_name = name
            if type(name) is list:
                target_name = name[0][2:].replace('-', '_')
            if target_name in self._arg_initializers[func.__name__]:
                argument_values = self._arg_initializers[func.__name__][target_name]
                if type(argument_values) is dict:
                    parser.description += f'\n\t{target_name} - {settings["help"]}'
                    should_be_required = True
                    if 'default' in settings and settings['default'] not in argument_values.values():
                        should_be_required = False
                        parser.set_defaults(**{f'{target_name}': settings['default']})
                        argument_values[target_name] = settings['default']
                    mutex_group = parser.add_mutually_exclusive_group(required=should_be_required)
                    for value in argument_values.items():
                        mutex_group.add_argument(f'--{make_kebab_case(value[0])}', f'-{make_kebab_case(value[0])[0]}',
                                                 dest=target_name, action='store_const', const=value[1],
                                                 help=f'Sets {target_name} to {value[1]}')
                elif type(argument_values) is list:
                    if 'default' in settings and settings['default'] not in argument_values:
                        argument_values.append(settings['default'])
                    if type(name) is list:
                        parser.add_argument(*name, **settings, choices=sorted(argument_values))
                    else:
                        parser.add_argument(name, **settings, choices=sorted(argument_values))
            else:
                if type(name) is list:
                    parser.add_argument(*name, **settings)
                else:
                    parser.add_argument(name, **settings)
        if self._use_logger:
            add_logging_flags(parser)
        parser.set_defaults(func=func)

    def register(self, *config_args, **config_kwargs):
        def registration_function(func: FunctionType):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            parameter_validation_exception = validate_parameters_in_docstring(func, self._silence)
            if parameter_validation_exception is not None:
                raise parameter_validation_exception
            self._functions.append(func)
            self._arg_initializers[func.__name__] = dict(config_arg for config_arg in
                                                         config_kwargs.items() if
                                                         config_arg[0] in get_argument_names(func))
            return wrapper

        return registration_function

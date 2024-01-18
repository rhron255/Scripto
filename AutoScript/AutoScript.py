import argparse
import functools
import logging
import pprint
import readline  # noqa # pylint: disable=unused-import
from types import FunctionType
from typing import List

from ArgumentParserExtensions import ExceptionThrowingArgumentParser, add_logging_flags, generate_parser_definitions, \
    generate_action_settings
from FuncUtils import validate_parameters_in_docstring, get_argument_names, make_kebab_case, strip_dict_to_func_args, \
    parse_dict_to_parameters
from StringUtils import print_intro, split_to_dict


class AutoScript:
    _description: str
    _silence: bool
    _functions: List[FunctionType] = []
    _arg_initializers = {}
    _use_logger = False
    _enable_interactive_mode = False
    _title_color = 'white'

    def __init__(self, description, suppress_warnings=False, auto_log=False, enable_interactive_mode=False,
                 title_color='white'):
        self._environment = {}
        self._description = description
        self._silence = suppress_warnings
        self._use_logger = auto_log
        self._enable_interactive_mode = enable_interactive_mode
        self._title_color = title_color

    def run(self):
        parser = self.build_parser()
        args = parser.parse_args()

        if args._interactive and '_func' not in args or '_force_interactive' in args and args._force_interactive:
            print_intro(self._description + '\nEnter "help" for assistance, or "exit" to leave!',
                        color=self._title_color)
            interactive_parser = self.build_parser(is_interactive=True, add_epilog=False, add_help=False,
                                                   exit_on_error=False)

            self._environment = {}
            while (command := input('> ')) != 'exit':
                if command == 'exit':
                    exit(0)
                else:
                    try:
                        interactive_args, invalid_options = interactive_parser.parse_known_args(command.split())
                    except argparse.ArgumentError as argparser_error:
                        print(argparser_error)
                    except argparse.ArgumentTypeError as argparser_error:
                        print(argparser_error)
                    except KeyboardInterrupt as key_interrupt:
                        print('Exiting...')
                        exit(0)
                    except Exception as generic_exception:
                        print(generic_exception)
                    else:
                        if len(invalid_options) > 0:
                            print(f'Invalid options provided:\n{",".join(invalid_options)}')
                        else:
                            try:
                                if '_action' in interactive_args:
                                    if interactive_args._action == 'set':
                                        variables = split_to_dict(' '.join(command.split()[1:]))
                                        pprint.pprint(variables)
                                        self._environment.update(variables)
                                    elif interactive_args._action == 'show':
                                        print('Environment:')
                                        pprint.pprint(self._environment)
                                    elif interactive_args._action == 'help':
                                        if interactive_args.function == [None]:
                                            print(self.prepare_help_msg(interactive_parser))
                                            print(
                                                'You can enter "help" to show this message again, or "exit" to leave!')
                                        else:
                                            target = interactive_args.function[0]
                                            target_subparser = interactive_parser._subparsers._group_actions[0].choices[
                                                target]
                                            target_subparser.epilog = ''
                                            print(self.prepare_help_msg(target_subparser))
                                            print(
                                                'You can enter "help" to show this message again, or "exit" to leave!')
                                else:
                                    self.run_args(interactive_args)
                            except KeyboardInterrupt as key_interrupt:
                                print('Exiting...')
                                exit(0)
                            except Exception as generic_exception:
                                print(generic_exception)
        else:
            self.run_args(args)

    def prepare_help_msg(self, parser):
        help_lines = parser.format_help().splitlines()[1:]
        return '\n'.join([line for line in help_lines if not line.strip().startswith('-h, --help')])

    def run_args(self, args):
        # Popping the function used out of the arguments passed to the function.
        func_args = {**vars(args)}
        if self._use_logger:
            logging.basicConfig(level=func_args.pop('log_level'))
        func = func_args.pop('_func')
        env_dict = parse_dict_to_parameters(func, self._environment)
        func_args.update(env_dict)
        func(**strip_dict_to_func_args(func, func_args))

    def build_parser(self, *args, add_epilog=True, is_interactive=False, **parser_kwargs):
        parser_settings = dict(description=self._description, conflict_handler='resolve',
                               formatter_class=argparse.RawDescriptionHelpFormatter)
        if is_interactive:
            parser = ExceptionThrowingArgumentParser(**parser_settings, **parser_kwargs)
        else:
            parser = argparse.ArgumentParser(**parser_settings, **parser_kwargs)

        parser.set_defaults(_interactive=self._enable_interactive_mode)
        if len(self._functions) == 0:
            raise ValueError('No functions registered...')
        if len(self._functions) == 1 and not is_interactive:
            function = self._functions[0]
            self.add_function_to_parser(function, parser)
            if self._enable_interactive_mode:
                parser.add_argument('--interactive', help='Sets the script to run in interactive mode.',
                                    dest='_force_interactive', action='store_true', default=False)
        else:
            sub = parser.add_subparsers(required=not self._enable_interactive_mode)
            for func in self._functions:
                name, settings = generate_parser_definitions(func, add_epilog=add_epilog)
                sub_parser = sub.add_parser(name, **settings, conflict_handler='resolve',
                                            formatter_class=argparse.RawDescriptionHelpFormatter, **parser_kwargs)
                self.add_function_to_parser(func, sub_parser)
            if is_interactive:
                set_help = 'Sets a number of variables for the environment.'
                set_parser = sub.add_parser('set', help=set_help, description=set_help)
                set_parser.add_argument('key_value', nargs='*', type=split_to_dict,
                                        help='The variables to set, in a "name"=value format.')
                set_parser.set_defaults(_action='set')
                show_help = 'Shows the values currently set in the environment.'
                show_parser = sub.add_parser('show', help=show_help, description=show_help)
                show_parser.set_defaults(_action='show')
                help_help = 'Prints the help message for the tool being used, or for the function supplied.'
                help_parser = sub.add_parser('help', help=help_help, description=help_help)
                help_parser.add_argument('function', nargs='*', default=[None],
                                         help='The function whose help message should be printed.')
                help_parser.set_defaults(_action='help')
        return parser

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
        parser.set_defaults(_func=func)

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

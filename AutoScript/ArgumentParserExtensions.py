import argparse
from types import FunctionType

from FuncUtils import get_parameters, make_kebab_case, get_description, get_first_doc_sentence


class ExceptionThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message: str):
        sub_name = self.prog.split()[1]
        self.exit(2, f'{sub_name}: error: {message}')

    def exit(self, status=0, message=None):
        if message:
            raise argparse.ArgumentError(message=message, argument=None)


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


def generate_action_settings(func: FunctionType):
    parameters = [param for param in get_parameters(func)]
    for param in parameters:
        settings = dict(type=param['type'], help=param['description'])
        if param['type'] is bool:
            name = param['name']
            param['name'] = []
            param['name'].append(f'--{make_kebab_case(name)}')
            param['name'].append(f'-{name[0]}')
            settings['action'] = 'store_true'
            settings.pop('type')
        if 'default' in param:
            name = param['name']
            param['name'] = []
            param['name'].append(f'--{make_kebab_case(name)}')
            param['name'].append(f'-{name[0]}')
            settings['default'] = param['default']
            settings['help'] += f' Defaults to {param["default"]} if not provided.'
        yield param['name'], settings


def generate_parser_definitions(func: FunctionType, add_epilog=True):
    return make_kebab_case(func.__name__), dict(description=get_description(func),
                                                help=get_first_doc_sentence(func),
                                                epilog=f'{"Automatically generated by AutoScript" if add_epilog else ""}')

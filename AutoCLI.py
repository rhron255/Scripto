import functools

from FuncUtils import generate_parser


def auto_cli(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        arg_parser = generate_parser(func)
        return func(**vars(arg_parser.parse_args()))

    return wrapper

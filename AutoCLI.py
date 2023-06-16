import functools

from FuncUtils import get_description, get_parameters


def auto_cli(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        docstring = get_description(func)
        parameters = [param for param in get_parameters(func)]
        print(docstring)
        print(parameters)
        return func(*args, **kwargs)

    return wrapper

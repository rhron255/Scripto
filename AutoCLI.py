import inspect, functools


def auto_cli(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        docstring = inspect.getdoc(func)
        signature = inspect.signature(func)
        print(docstring)
        print(signature.parameters)
        return func(*args, **kwargs)
    return wrapper

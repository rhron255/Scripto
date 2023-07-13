# A test document with function stubs to test
from AutoCLI import auto_cli, AutoCli

app = AutoCli("Test")


@auto_cli()
def test_func(param_a: int, param_b: int):
    """
    Some fancy doctstring describing the function.
    :param param_a: The first parameter passed to the function.
    :param param_b: The second parameter passed to the function.
    :return: Nothing
    """
    pass


# @auto_cli
def fail_func(param_a: int, param_b: int):
    """
    Some fancy doctstring describing the function.
    :param param_a: The first parameter passed to the function.
    :return: Nothing
    """
    pass


@auto_cli()
def bool_func(b: bool):
    """
    Funky
    :param b: does stuff
    :return: Nope
    """
    print("success" if b else "failure")


if __name__ == '__main__':
    app.run()

# A test document with function stubs to test
from AutoCLI import auto_cli


@auto_cli
def test_func(param_a: int, param_b: int):
    """
    Some fancy doctstring describing the function.
    :param param_a: The first parameter passed to the function.
    :param param_b: The second parameter passed to the function.
    :return: Nothing
    """
    pass


if __name__ == '__main__':
    test_func(1, 2)

# A test document with function stubs to test
from AutoScript.AutoScript import AutoScript

script = AutoScript("Test",
                    suppress_warnings=True,
                    auto_log=True,
                    enable_interactive_mode=True)


@script.register(param_a={'a': 1, 'aa': 2, 'aaa': 3}, param_b=[1, 2, 3])
def test_func(param_a: int = 0, param_b: int = 5):
    """
    Some fancy docstring describing the function.
    :param param_a: The first parameter passed to the function.
    :return: Nothing
    """
    print(param_a + param_b)


# @auto_cli
def fail_func(param_a: int, param_b: int):
    """
    Some fancy doctstring describing the function.
    :param param_a: The first parameter passed to the function.
    :return: Nothing
    """
    pass


@script.register()
def bool_func(super_long_parameter_name: bool):
    """
    Funky
    :param super_long_parameter_name: does stuff
    :return: Nope
    """
    print("success" if super_long_parameter_name else "failure")


if __name__ == '__main__':
    script.run()

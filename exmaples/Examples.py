# A test document with function stubs to test
from scripto.app import Scripto

script = Scripto("Test",
                 suppress_warnings=True,
                 auto_log=True)


@script.register(param_a={'one': 1, 'two': 2, 'three': 3}, param_b=[0, 1, 2, 3])
def test_func(param_a: int = 0, param_b: int = 5):
    """
    Some fancy docstring describing the function.
    The registration parameters will create unique flags for the parameters,
    using the provided names for the options, as such:
    --one (to set the value of param_a to 1)
    --two (to set the value of param_a to 2)
    --three (to set the value of param_a to 3)
    :param param_a: The first parameter passed to the function.
    :param param_b: Another parameter
    :return: Nothing
    """
    print(f'a: {param_a}, b: {param_b}')


@script.register()
def bool_func(super_long_parameter_name: bool):
    """
    Funky
    :param super_long_parameter_name: does stuff
    :return: Nope
    """
    print("success" if super_long_parameter_name else "failure")


@script.register()
def list_func(opt_arg: list[str] = ("one", "two", "three")):
    """
    Takes all command line arguments and prints them!
    :param opt_arg: A list of strings to print
    """
    print(','.join(opt_arg))


if __name__ == '__main__':
    script.run()

from types import FunctionType


class FunctionData:
    """
    Convenience holder for function data, to be used later for parsing data.
    """

    function: FunctionType
    name: str

    def __init__(self, function: FunctionType, name: str = None):
        self.function = function
        self.name = name

    def func(self) -> FunctionType:
        # noinspection PyTypeChecker
        return self.function

from types import FunctionType


class FunctionData:
    """
    Convenience holder for function data, to be used later for parsing data.
    """

    function: FunctionType
    name: str
    aliases: list[str]

    def __init__(
        self, function: FunctionType, name: str = None, aliases: list[str] = None
    ):
        self.function = function
        self.name = name
        self.aliases = aliases

    def func(self) -> FunctionType:
        # noinspection PyTypeChecker
        return self.function

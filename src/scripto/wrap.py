import os.path
from scripto.app import Scripto

script = Scripto('Module Wrapper Utility')

module_template = """
from scripto.app import Scripto
import $MODULE_NAME
script = Scripto("$CAP_MODULE_NAME Wrapper", suppress_warnings=True)

functions = [
    eval(f"$MODULE_NAME.{func}")
    for func in dir($MODULE_NAME)
    if eval(f"type($MODULE_NAME.{func})").__name__ == "function" and not func.startswith("_")
]
for func in functions:
    script.register()(func)
script.run()

"""

func_template = """
from scripto.app import Scripto
import $MODULE_NAME
script = Scripto("$CAP_MODULE_NAME Wrapper", suppress_warnings=True)

functions = [
    eval(f"$MODULE_NAME.{func}")
    for func in dir($MODULE_NAME)
    if eval(f"type($MODULE_NAME.{func})").__name__ == "function" and not func.startswith("_") and eval(f"$MODULE_NAME.{func}").__name__ == "$FUNC_NAME"
]
for func in functions:
    script.register()(func)
script.run()

"""


@script.register()
def wrap(module_name: str, output_path: str = os.path.expanduser('~/scripto'), function_name: str = None):
    """
    Automatically generates a script wrapping a module, and places it under a 'scripto' directory in the user's home folder.
    :param module_name: The name of the module to wrap.
    :param output_path: The path to place the script in.
    :param function_name: A single function to wrap within a module. If not supplied wraps the entire module.
    :return: None
    """""
    if not (os.path.exists(output_path) and os.path.isdir(output_path)):
        os.makedirs(output_path, exist_ok=True)
    if function_name:
        with open(os.path.join(output_path, f'{function_name}.py'), 'w') as sc_file:
            named_template = func_template.replace('$CAP_MODULE_NAME', module_name.upper())
            named_template = named_template.replace('$FUNC_NAME', function_name)
            sc_file.write(named_template.replace('$MODULE_NAME', module_name))
    else:
        with open(os.path.join(output_path, f'auto_{module_name}.py'), 'w') as sc_file:
            named_template = module_template.replace('$CAP_MODULE_NAME', module_name.upper())
            sc_file.write(named_template.replace('$MODULE_NAME', module_name))


if __name__ == '__main__':
    script.run()

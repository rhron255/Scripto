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
script = Scripto("$CAP_FUNC_NAME Wrapper", suppress_warnings=True)
script.register()($MODULE_NAME.$FUNC_NAME)
script.run()
"""


@script.register()
def wrap(module_name: str, output_path: str = os.path.expanduser('~/scripto'), function_level=True):
    if not function_level:
        if not (os.path.exists(output_path) and os.path.isdir(output_path)):
            os.makedirs(output_path, exist_ok=True)
        with open(os.path.join(output_path, f'{module_name}.py'), 'w') as sc_file:
            named_template = module_template.replace('$CAP_MODULE_NAME', module_name.upper())
            sc_file.write(named_template.replace('$MODULE_NAME', module_name))
    else:
        functions = [
            eval(f"{module_name}.{func}") for func in dir(module_name) if not func.startswith("_") and eval(f"type({module_name}.{func})").__name__ == "function"
        ]
        for func in functions:
            with open(os.path.join(output_path, f'{func.__name__}.py'), 'w') as sc_file:
                named_template = func_template.replace('$MODULE_NAME', module_name)
                named_template = named_template.replace('$FUNC_NAME', func.__name__)
                named_template = named_template.replace('$CAP_FUNC_NAME', func.__name__.upper())
                sc_file.write()


if __name__ == '__main__':
    script.run()

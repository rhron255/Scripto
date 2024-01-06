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


@script.register()
def wrap(module_name: str, output_path: str = os.path.expanduser('~/scripto')):
    if not (os.path.exists(output_path) and os.path.isdir(output_path)):
        os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, f'{module_name}.py'), 'w') as sc_file:
        named_template = module_template.replace('$CAP_MODULE_NAME', module_name.upper())
        sc_file.write(named_template.replace('$MODULE_NAME', module_name))


if __name__ == '__main__':
    script.run()

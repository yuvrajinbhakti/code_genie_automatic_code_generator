from typing import List, Dict, Any
import argparse
import autopep8

def safe_input(prompt, expected_type=str, default=None):
    while True:
        user_input = input(prompt).strip()
        if not user_input and default is not None:
            return default
        try:
            if expected_type == int:
                return int(user_input)
            elif expected_type == float:
                return float(user_input)
            elif expected_type == list:
                return [item.strip() for item in user_input.split(',')]
            else:
                return user_input
        except ValueError:
            print(f"Invalid input. Please enter a value of type {expected_type.__name__}.")

def validated_choice(prompt, options):
    while True:
        choice = input(prompt).strip().lower()
        if choice in options:
            return choice
        print(f"Invalid choice. Please choose from {', '.join(options)}.")

def generate_function_signature(func_name, params, return_type=None, decorators=None):
    param_str = ', '.join([f"{param['name']}: {param['type']} = {param['default']}" if 'default' in param else f"{param['name']}: {param['type']}" for param in params])
    return_type_str = f" -> {return_type}" if return_type else ""
    decorator_str = '\n'.join([f"@{decorator}" for decorator in decorators]) if decorators else ""
    return f"{decorator_str}\ndef {func_name}({param_str}){return_type_str}:"

def generate_function_logic(logic):
    indented_logic = '\n    '.join(logic.split('\n'))
    return f"    {indented_logic}"

def generate_docstring(params, return_type):
    param_str = '\n'.join([f"    :param {param['type']} {param['name']}: Description" for param in params])
    return_type_str = f"\n    :return: {return_type} -- Description" if return_type else ""
    return f'    """\n    {param_str}{return_type_str}\n    """\n'

def generate_function(func_name, params, logic, return_type=None, docstring=None, decorators=None):
    signature = generate_function_signature(func_name, params, return_type, decorators)
    docstring = docstring or generate_docstring(params, return_type)
    function_code = f"{signature}\n{docstring}{generate_function_logic(logic)}"
    return function_code

def generate_class(class_name, attributes=None, methods=None):
    attributes = attributes or []
    methods = methods or []
    
    class_signature = f"class {class_name}:"
    
    if attributes:
        init_params = [{'name': attr['name'], 'type': attr.get('type', 'Any')} for attr in attributes]
        init_logic = '\n'.join([f"self.{attr['name']} = {attr['name']}" for attr in attributes])
        init_method = generate_function('__init__', init_params, init_logic)
        methods.insert(0, init_method)
    
    if not methods:
        return f"{class_signature}\n    pass"
    
    class_code = f"{class_signature}\n"
    for method in methods:
        indented_method = '\n    '.join(method.split('\n'))
        class_code += f"    {indented_method}\n\n"
    
    return class_code

def generate_custom_exception(exception_name, base_exception='Exception'):
    return f"class {exception_name}({base_exception}):\n    pass\n"

def generate_factory_method(class_name, params):
    param_str = ', '.join([f"{param['name']}: {param['type']}" if param['type'] else param['name'] for param in params])
    logic = f"return {class_name}({', '.join([param['name'] for param in params])})"
    return generate_function(f"create_{class_name.lower()}", params, logic, return_type=class_name)

def generate_overloaded_method(func_name, signatures, logic_blocks):
    method_code = ""
    for i, (params, logic) in enumerate(zip(signatures, logic_blocks)):
        condition = " and ".join([f"isinstance({param['name']}, {param['type']})" for param in params if param['type']])
        logic_code = generate_function_logic(logic)
        method_code += f"if {condition}:\n    {logic_code}\n"
        if i < len(signatures) - 1:
            method_code += "elif "
    return generate_function_signature(func_name, signatures[0]) + "\n" + method_code

def generate_test_function(func_name, params):
    test_func_name = f"test_{func_name}"
    test_logic = f"assert {func_name}({', '.join([param['test_value'] for param in params])}) == EXPECTED_OUTPUT"
    return generate_function(test_func_name, [], test_logic)

def format_code(code):
    return autopep8.fix_code(code)

def parse_args():
    parser = argparse.ArgumentParser(description="Generate Python code")
    parser.add_argument('-t', '--type', choices=['function', 'class', 'exception'], required=True, help="Type of code to generate")
    parser.add_argument('-n', '--name', required=True, help="Name of the function, class, or exception")
    parser.add_argument('-p', '--params', nargs='*', help="Parameters (name:type[:default]) for the function or method")
    parser.add_argument('-r', '--return_type', help="Return type for the function")
    parser.add_argument('-l', '--logic', help="Logic of the function or method")
    parser.add_argument('-d', '--docstring', help="Docstring for the function or method")
    parser.add_argument('-o', '--output', help="Output file name")
    return parser.parse_args()

def main():
    args = parse_args()
    
    params = [{'name': param.split(':')[0], 
               'type': param.split(':')[1] if ':' in param else 'Any',
               'default': param.split(':')[2] if len(param.split(':')) > 2 else None} 
              for param in args.params] if args.params else []

    if args.type == 'function':
        logic = args.logic or safe_input("Enter the function logic: ")
        generated_code = generate_function(args.name, params, logic, args.return_type, args.docstring)
    
    elif args.type == 'class':
        generated_code = generate_class(args.name, params)
    
    elif args.type == 'exception':
        generated_code = generate_custom_exception(args.name)
    
    else:
        print("Invalid type specified.")
        return
    
    formatted_code = format_code(generated_code)
    
    output_file = args.output or f"{args.name}.py"
    with open(output_file, "w") as file:
        file.write(formatted_code)
    print(f"Code saved to '{output_file}'")

if __name__ == "__main__":
    main()

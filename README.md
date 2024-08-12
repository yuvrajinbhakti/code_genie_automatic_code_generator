# CodeGenie

**CodeGenie** is a Python code generation tool that allows you to automatically create Python functions, classes, exceptions, and test cases. This tool is designed to simplify and automate code creation by generating well-structured and formatted Python code based on user input.

## Features

- **Generate Functions**: Create Python functions with customizable parameters, return types, decorators, and logic.
- **Generate Classes**: Define Python classes with attributes and methods, including factory methods.
- **Generate Custom Exceptions**: Create custom exception classes for your applications.
- **Generate Test Functions**: Automatically generate test functions for validating other functions.
- **Code Formatting**: Automatically formats generated code to adhere to PEP 8 standards using `autopep8`.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/codegenie.git
    cd codegenie
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The `codeGenie.py` script can be used from the command line to generate code snippets. Here’s how to use it:

### Command-Line Arguments

- `-t` or `--type`: The type of code to generate. Options are `function`, `class`, or `exception`.
- `-n` or `--name`: The name of the function, class, or exception.
- `-p` or `--params`: Parameters for the function or method in the format `name:type[:default]`.
- `-r` or `--return_type`: Return type for the function (optional).
- `-l` or `--logic`: Logic of the function or method (required for functions).
- `-d` or `--docstring`: Docstring for the function or method (optional).
- `-o` or `--output`: Output file name for the generated code.

### Examples

1. **Generate a Function**:
    ```bash
    python codeGenie.py -t function -n my_function -p name:str,age:int:25 -r str -l "return f'Name: {name}, Age: {age}'" -d "Returns a formatted string with name and age" -o my_function.py
    ```

2. **Generate a Class**:
    ```bash
    python codeGenie.py -t class -n MyClass -p name:str,age:int -o MyClass.py
    ```

3. **Generate a Custom Exception**:
    ```bash
    python codeGenie.py -t exception -n MyCustomException -o MyCustomException.py
    ```

## Code Formatting

Generated code is automatically formatted using `autopep8` to ensure it adheres to PEP 8 standards.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please fork the repository and submit a pull request.


import os
import inspect
import textwrap
import re
from typing import Callable, get_origin, get_args

def register_gemini_skill(func: Callable):
    """
    Generates the necessary files for a Gemini CLI skill from a Python function.
    The generated files (main.py and tool.toml) will be placed in a subdirectory
    within '_generated_skills/' in the current working directory.

    The user is responsible for manually moving these generated files to
    'C:\Usersando\.gemini\skills' for global use.

    Args:
        func: The Python function to convert into a Gemini skill.
              The function should have a docstring for description and
              type hints for parameter definitions.
    """
    skill_name = func.__name__.replace('_', '-')
    skill_dir = os.path.join('_generated_skills', skill_name)
    os.makedirs(skill_dir, exist_ok=True)

    # 1. Generate main.py with the function's source code
    func_source = textwrap.dedent(inspect.getsource(func))
    main_py_path = os.path.join(skill_dir, 'main.py')
    with open(main_py_path, 'w') as f:
        f.write(func_source)
    print(f"Generated {main_py_path}")

    # 2. Generate tool.toml for skill metadata
    tool_toml_path = os.path.join(skill_dir, 'tool.toml')
    
    # Extract description from docstring
    description = inspect.getdoc(func) or f"A skill based on the '{func.__name__}' Python function."
    description = description.split('

')[0].strip() # Take first paragraph as description

    # Extract parameters from type hints and docstring
    params = inspect.signature(func).parameters
    toml_params = []
    
    for name, param in params.items():
        if name == 'self': # Skip 'self' in methods
            continue
        
        param_type = 'string' # Default type
        if param.annotation is not inspect.Parameter.empty:
            # Handle common types
            if param.annotation in (str, int, float, bool):
                param_type = param.annotation.__name__.lower()
            elif get_origin(param.annotation) is list:
                param_type = 'array'
            elif get_origin(param.annotation) is dict:
                param_type = 'object'
            # Add more type mappings as needed
        
        # Try to find parameter description in docstring
        param_description = ""
        if func.__doc__:
            # Regex to find description for 'name' in docstring
            # Looks for ':param name: Description' or 'name (type): Description'
            match = re.search(rf"(?::param\s*{name}:\s*(.*?)
|{name}\s*\(.*?\):\s*(.*?)
)", func.__doc__, re.IGNORECASE)
            if match:
                param_description = (match.group(1) or match.group(2)).strip()
        
        toml_params.append(f"""
    [[params]]
    name = "{name}"
    type = "{param_type}"
    description = "{param_description if param_description else f'The {name} parameter.'}"
    required = {str(param.default is inspect.Parameter.empty).lower()}
""")

    toml_content = f"""
[tool]
name = "{skill_name}"
description = "{description}"

{"".join(toml_params)}
"""
    with open(tool_toml_path, 'w') as f:
        f.write(toml_content.strip())
    print(f"Generated {tool_toml_path}")

    print(f"
Skill '{skill_name}' generated in '{skill_dir}'.")
    print(f"To use this skill globally, please manually copy the contents of '{skill_dir}'")
    print(f"to 'C:\Usersando\.gemini\skills\{skill_name}'")

if __name__ == '__main__':
    # Example usage:
    def example_skill_function(
        file_path: str,
        content: str,
        overwrite: bool = False
    ) -> bool:
        """
        Writes content to a specified file.

        :param file_path: The path to the file to write to.
        :param content: The content to write.
        :param overwrite: If true, overwrite the file if it exists.
                          Otherwise, append content.
        :return: True if write was successful, False otherwise.
        """
        # This function body is just a placeholder; the actual implementation
        # would be in the original function that this script processes.
        print(f"Simulating writing to {file_path}")
        return True

    # To run this example, save this script as register_gemini_skill.py
    # then in a Python interpreter or another script:
    # from register_gemini_skill import register_gemini_skill, example_skill_function
    # register_gemini_skill(example_skill_function)
    print("This script is designed to be imported and used with a function object.")
    print("An example function 'example_skill_function' is included for demonstration purposes.")
    print("To register this example, you would typically run:")
    print("  from register_gemini_skill import register_gemini_skill, example_skill_function")
    print("  register_gemini_skill(example_skill_function)")


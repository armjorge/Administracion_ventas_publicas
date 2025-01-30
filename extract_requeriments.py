import os
import importlib.util

# Set the directory where your scripts are located
script_directory = os.path.dirname(os.path.abspath(__file__))
working_folder = os.path.abspath(os.path.join(script_directory, '..'))
function_library = os.path.abspath(os.path.join(script_directory, 'Library'))

# Collect all Python scripts
all_scripts = []
for root, _, files in os.walk(script_directory):
    for file in files:
        if file.endswith(".py"):
            all_scripts.append(os.path.join(root, file))

# Extract all imported modules
imported_modules = set()
for script in all_scripts:
    with open(script, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("import ") or line.startswith("from "):
                parts = line.split()
                module_name = parts[1].split(".")[0]  # Get base module
                imported_modules.add(module_name)

# Check which modules are external (installed via pip)
external_modules = set()
for module in imported_modules:
    if importlib.util.find_spec(module) is not None:
        try:
            # Check if it's a built-in Python module
            if importlib.util.find_spec(module) is None:
                continue  # Skip built-in modules
            external_modules.add(module)
        except ModuleNotFoundError:
            continue

# Save to requirements.txt
with open("requirements.txt", "w") as f:
    for module in external_modules:
        f.write(f"{module}\n")

print("✅ External dependencies saved in requirements.txt")
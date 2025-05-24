import os
import sys
from pathlib import Path

# Get the parent directory (fabricatio workspace root)
parent_dir = Path.cwd().parent

# Read the parent pyproject.toml
pyproject_path = parent_dir / "pyproject.toml"

if pyproject_path.exists():
    import tomllib
    
    # Load the pyproject.toml
    with open(pyproject_path, "r") as f:
        pyproject_data = tomllib.load(f)
    
    # Get project name from cookiecutter
    project_name = "{{ cookiecutter.project_name }}"
    full_name = "{{ cookiecutter.full_name }}"
    
    # Update optional dependencies
    if "project" not in pyproject_data:
        pyproject_data["project"] = {}
    if "optional-dependencies" not in pyproject_data["project"]:
        pyproject_data["project"]["optional-dependencies"] = {}
    
    # Add to full dependencies
    if "full" in pyproject_data["project"]["optional-dependencies"]:
        full_deps = pyproject_data["project"]["optional-dependencies"]["full"]
        # Extract the main fabricatio dependency
        main_dep = None
        for dep in full_deps:
            if dep.startswith("fabricatio["):
                main_dep = dep
                break
        
        if main_dep:
            # Add our project to the list of extras
            extras_start = main_dep.find("[") + 1
            extras_end = main_dep.find("]")
            extras = main_dep[extras_start:extras_end].split(",")
            extras.append(project_name)
            new_main_dep = f"fabricatio[{','.join(extras)}]"
            full_deps[full_deps.index(main_dep)] = new_main_dep
    
    # Add new optional dependency group
    pyproject_data["project"]["optional-dependencies"][project_name] = [full_name]
    
    # Update tool.uv.sources
    if "tool" not in pyproject_data:
        pyproject_data["tool"] = {}
    if "uv" not in pyproject_data["tool"]:
        pyproject_data["tool"]["uv"] = {}
    if "sources" not in pyproject_data["tool"]["uv"]:
        pyproject_data["tool"]["uv"]["sources"] = {}
    
    pyproject_data["tool"]["uv"]["sources"][full_name] = {"workspace": True}
    
    # Write back the updated pyproject.toml
    with open(pyproject_path, "w") as f:
        tomllib.dump(pyproject_data, f)
    
    print(f"Successfully registered {full_name} in the workspace pyproject.toml")
else:
    print("Warning: Parent pyproject.toml not found. Skipping registration.")



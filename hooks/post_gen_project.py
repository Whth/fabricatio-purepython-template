"""
This is a cookiecutter template `post_gen_project.py` for creating a new project.

{

  "project_name": "demo",
  "ecosystem": "fabricatio",
  "full_name": "{{ cookiecutter.ecosystem }}-{{ cookiecutter.project_name }}",
  "package_name": "{{ cookiecutter.ecosystem }}_{{ cookiecutter.project_name }}",
  "description": "An extension of fabricatio."
}


i need add the extension to the root pyproject file

add source mark
```toml
[tool.uv.sources]
fabricatio = { workspace = true }
fabricatio-core = { workspace = true }
fabricatio-capabilities = { workspace = true }
fabricatio-actions = { workspace = true }
fabricatio-typst = { workspace = true }
fabricatio-rag = { workspace = true }
fabricatio-rule = { workspace = true }
fabricatio-judge = { workspace = true }
fabricatio-improve = { workspace = true }
fabricatio-digest = { workspace = true }
fabricatio-memory = { workspace = true }
fabricatio-anki = { workspace = true }
fabricatio-{{ cookiecutter.project_name }} = { workspace = true }
```


register optional-dependencies

```toml
[project.optional-dependencies]
full = [
    "fabricatio[rag,cli,typst,rule,judge,capabilities,actions,improve,digest,memory,anki,{{  cookiecutter.project_name }}]",
]

{{  cookiecutter.project_name }} = [
    "fabricatio-{{ cookiecutter.project_name }}"
]

anki = [
    "fabricatio-anki"
]

memory = [
    "fabricatio-memory",
]
digest = [
    "fabricatio-digest",
]
rag = [
    "fabricatio-rag",
]

judge = [
    "fabricatio-judge",
]


rule = [
    "fabricatio-rule",
]


cli = [
    "typer-slim[standard]>=0.15.2",
]


typst = [
    "fabricatio-typst",
]

improve = [
    "fabricatio-improve",
]

capabilities = [
    "fabricatio-capabilities",
]

actions = [
    "fabricatio-actions",
]

```
"""

from pathlib import Path

import tomlkit

# Get the project name from the cookiecutter context
project_name = "{{ cookiecutter.project_name }}"

# Path to the root pyproject.toml file (assuming it's in the parent directory)
pyproject_path:Path = Path.cwd().parent.parent/"pyproject.toml"

if not pyproject_path.exists():
    print(f"Warning: {pyproject_path} not found")
    exit(1)


doc = tomlkit.parse(pyproject_path.read_text("utf-8"))

# Add to [tool.uv.sources]
if "tool" not in doc:
    doc["tool"] = tomlkit.table()
if "uv" not in doc["tool"]:
    doc["tool"]["uv"] = tomlkit.table()
if "sources" not in doc["tool"]["uv"]:
    doc["tool"]["uv"]["sources"] = tomlkit.table()

# Add the new project source with inline table format
sources_table = doc["tool"]["uv"]["sources"]
inline_table = tomlkit.inline_table()
inline_table["workspace"] = True
sources_table[f"fabricatio-{project_name}"] = inline_table

# Add to [project.optional-dependencies]
if "project" not in doc:
    doc["project"] = tomlkit.table()
if "optional-dependencies" not in doc["project"]:
    doc["project"]["optional-dependencies"] = tomlkit.table()

# Add the new project dependency
doc["project"]["optional-dependencies"][project_name] = [f"fabricatio-{project_name}"]

# Update the full dependency list to include the new project
if "full" in doc["project"]["optional-dependencies"]:
    full_deps = doc["project"]["optional-dependencies"]["full"]
    if isinstance(full_deps, list) and len(full_deps) > 0:
        # Find the fabricatio dependency and update it
        for i, dep in enumerate(full_deps):
            if isinstance(dep, str) and dep.startswith("fabricatio["):
                # Extract the current extras
                start = dep.find("[") + 1
                end = dep.find("]")
                if start > 0 and end > start:
                    current_extras = dep[start:end]
                    # Add the new project to the extras
                    new_extras = f"{current_extras},{project_name}"
                    full_deps[i] = f"fabricatio[{new_extras}]"
                    break

# Write the updated pyproject.toml
with open(pyproject_path, "w", encoding="utf-8") as f:
    f.write(tomlkit.dumps(doc))

print(f"Successfully updated {pyproject_path} with fabricatio-{project_name}")


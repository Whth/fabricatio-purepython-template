from pathlib import Path

# Get the parent directory (fabricatio workspace root)
parent_dir = Path.cwd().parent

# Read the parent pyproject.toml
pyproject_path = parent_dir / "pyproject.toml"

if pyproject_path.exists():
    # Read the pyproject.toml file
    with open(pyproject_path, "r") as f:
        content = f.read()
    
    # Get project name from cookiecutter
    project_name = "{{ cookiecutter.project_name }}"
    full_name = "{{ cookiecutter.full_name }}"
    
    # Find and update the fabricatio dependency in full section
    lines = content.split('\n')
    new_lines = []
    in_full_section = False
    full_section_updated = False
    
    for i, line in enumerate(lines):
        if line.strip() == 'full = [':
            in_full_section = True
            new_lines.append(line)
        elif in_full_section and line.strip() == ']':
            in_full_section = False
            new_lines.append(line)
        elif in_full_section and 'fabricatio[' in line and not full_section_updated:
            # Extract and update the fabricatio dependency
            start_idx = line.find('fabricatio[') + len('fabricatio[')
            end_idx = line.find(']', start_idx)
            if start_idx > len('fabricatio[') - 1 and end_idx > start_idx:
                extras = line[start_idx:end_idx]
                extras_list = [e.strip() for e in extras.split(',') if e.strip()]
                if project_name not in extras_list:
                    extras_list.append(project_name)
                new_extras = ','.join(extras_list)
                new_line = line[:start_idx] + new_extras + line[end_idx:]
                new_lines.append(new_line)
                full_section_updated = True
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    # Add new optional dependency section if not exists
    content = '\n'.join(new_lines)
    if f'[project.optional-dependencies.{project_name}]' not in content:
        # Find where to insert the new section
        insert_idx = content.find('[tool.')
        if insert_idx == -1:
            insert_idx = len(content)
        
        new_section = f'\n[project.optional-dependencies.{project_name}]\n{project_name} = ["{full_name}"]\n'
        content = content[:insert_idx] + new_section + content[insert_idx:]
    
    # Add tool.uv.sources entry
    if '[tool.uv.sources]' not in content:
        # Add the entire section
        sources_section = f'\n[tool.uv.sources]\n{full_name} = {{ workspace = true }}\n'
        content = content.rstrip() + sources_section
    else:
        # Find the sources section and add our entry
        sources_idx = content.find('[tool.uv.sources]')
        if sources_idx != -1:
            # Find the next section or end of file
            next_section_idx = content.find('\n[', sources_idx + 1)
            if next_section_idx == -1:
                next_section_idx = len(content)
            
            # Insert before the next section
            insert_point = next_section_idx
            while insert_point > 0 and content[insert_point - 1] in '\n\r':
                insert_point -= 1
            
            new_entry = f'{full_name} = {{ workspace = true }}\n'
            content = content[:insert_point] + new_entry + content[insert_point:]
    
    # Write back the updated pyproject.toml
    with open(pyproject_path, "w") as f:
        f.write(content)
    
    print(f"Successfully registered {full_name} in the workspace pyproject.toml")
else:
    print("Warning: Parent pyproject.toml not found. Skipping registration.")
"""Module containing configuration classes for {{ cookiecutter.full_name }}."""
from dataclasses import dataclass
from fabricatio_core import CONFIG
@dataclass
class {{ cookiecutter.project_name|capitalize }}Config:
    """ Configuration for {{ cookiecutter.full_name }}"""



{{ cookiecutter.project_name }}_config = CONFIG.load("{{ cookiecutter.project_name }}",  {{ cookiecutter.project_name|capitalize }}Config)
__all__ = [
    "{{ cookiecutter.project_name }}_config"
]
"""Tests for the {{ cookiecutter.project_name }}."""
import pytest
from fabricatio_mock.models.mock_role import LLMTestRole
from {{cookiecutter.package_name}}.capabilities.{{cookiecutter.project_name}} import {{ cookiecutter.project_name | capitalize}}


class {{ cookiecutter.project_name | capitalize}}Role(LLMTestRole, {{ cookiecutter.project_name | capitalize}}):
    """Test role that combines LLMTestRole with {{ cookiecutter.project_name | capitalize}} for testing."""

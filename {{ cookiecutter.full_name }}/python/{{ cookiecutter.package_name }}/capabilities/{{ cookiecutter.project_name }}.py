"""This module contains the capabilities for the {{ cookiecutter.project_name }}."""
from fabricatio_core.capabilities.usages import UseLLM



class {{ cookiecutter.project_name | capitalize}}(UseLLM):
    """This class contains the capabilities for the {{ cookiecutter.project_name }}."""

    async def {{cookiecutter.project_name}}(self, **kwargs): ...

"""Template rendering for the Catchpoint Configurator."""

import os
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader
from jinja2 import TemplateError as Jinja2TemplateError

from .exceptions import TemplateError


def render_template(template_name: str, context: Dict[str, Any]) -> str:
    """Render a template with the given context.

    Args:
        template_name: Template name
        context: Template context

    Returns:
        Rendered template string

    Raises:
        TemplateError: If template rendering fails
    """
    try:
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        template = env.get_template(template_name)
        return template.render(**context)
    except Jinja2TemplateError as e:
        raise TemplateError(
            f"Failed to render template {template_name}: {str(e)}",
            {"template": template_name, "context": context},
        )

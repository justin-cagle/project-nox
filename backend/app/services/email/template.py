"""
Email template rendering utilities using Jinja2.

This module supports dual-format (HTML + plain text) template resolution
based on a shared base name. Templates are expected to live in the
`templates/` directory adjacent to this file.

If neither HTML nor text template is found for a given name, a ValueError is raised.
"""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

# Default directory for email templates
DEFAULT_TEMPLATE_DIR = Path(__file__).parent / "templates"


def get_env(base_dir: Path = DEFAULT_TEMPLATE_DIR) -> Environment:
    """
    Create a Jinja2 Environment for the given base directory.

    Args:
        base_dir (Path): Directory containing the templates.

    Returns:
        Jinja2 Environment instance configured with autoescaping enabled.
    """
    return Environment(loader=FileSystemLoader(str(base_dir)), autoescape=True)


def render_dual_template(
    template_name: str, context: dict, base_dir: Path = DEFAULT_TEMPLATE_DIR
) -> tuple[str, str]:
    """
    Render both HTML and plain-text versions of an email template.

    Args:
        template_name (str): Base name of the template file (without extension).
        context (dict): Variables passed into the template for rendering.
        base_dir (Path): Directory where template files are located.

    Returns:
        tuple[str, str]: (html_body, text_body). Either may be None if not found.

    Raises:
        ValueError: If neither template variant is found.
    """
    env = get_env(base_dir)

    # Attempt to render HTML version: template_name.html
    try:
        html_template = env.get_template(f"{template_name}.html")
        html_body = html_template.render(**context)
    except TemplateNotFound:
        html_body = None

    # Attempt to render plain text version: template_name.txt
    try:
        text_template = env.get_template(f"{template_name}.txt")
        text_body = text_template.render(**context)
    except TemplateNotFound:
        text_body = None

    # Fail if neither version exists
    if (not html_body) and (not text_body):
        raise ValueError(f"No templates found for {template_name}")

    return html_body, text_body

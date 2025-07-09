from pathlib import Path

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

DEFAULT_TEMPLATE_DIR = Path(__file__).parent / "templates"


def get_env(base_dir: Path = DEFAULT_TEMPLATE_DIR) -> Environment:
    return Environment(loader=FileSystemLoader(str(base_dir)), autoescape=True)


def render_dual_template(
    template_name: str, context: dict, base_dir: Path = DEFAULT_TEMPLATE_DIR
) -> tuple[str, str]:
    env = get_env(base_dir)

    try:
        html_template = env.get_template(f"{template_name}.html")
        html_body = html_template.render(**context)
    except TemplateNotFound:
        html_body = None

    try:
        text_template = env.get_template(f"{template_name}.txt")
        text_body = text_template.render(**context)
    except TemplateNotFound:
        text_body = None

    if (not html_body) and (not text_body):
        raise ValueError(f"No templates found for {template_name}")

    return html_body, text_body

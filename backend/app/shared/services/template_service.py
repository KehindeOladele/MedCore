from jinja2 import (
    Environment, 
    FileSystemLoader, 
    select_autoescape
)
from pathlib import Path


# ----- Initialize template environment -----
BASE_DIR = Path(__file__).resolve().parents[2]  # adjust if needed

TEMPLATE_DIR = BASE_DIR / "shared" / "email" / "template"

env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(["html", "xml"])
)


# ----- Render Welcome Patient HTML Template -----
def render_template(
    template_name: str,
    context: dict
):

    template = env.get_template(template_name)

    return template.render(**context)
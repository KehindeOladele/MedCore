from jinja2 import Environment, FileSystemLoader


# ----- Initialize template environment -----
env = Environment(
    loader=FileSystemLoader("app/templates")
)


# ----- Render Welcome Patient HTML Template -----
def render_template(
    template_name: str,
    context: dict
):

    template = env.get_template(template_name)

    return template.render(**context)
import jinja2
import os

default_loader = jinja2.FileSystemLoader(os.path.abspath("."))


environments = {
    "default": jinja2.Environment(loader=default_loader),
    "latex": jinja2.Environment(
        block_start_string="\BLOCK{",
        block_end_string="}",
        variable_start_string="\VAR{",
        variable_end_string="}",
        comment_start_string="\#{",
        comment_end_string="}",
        line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        autoescape=False,
        loader=default_loader,
    ),
}


def render(template_file, environment, **kwargs):
    env = environments[environment]
    template = env.get_template(template_file)
    return template.render(**kwargs)

def render_string(template_str, environment, **kwargs):
    env = environments[environment]
    template = env.from_string(template_str)
    return template.render(**kwargs)


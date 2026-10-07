"""Jinja2 environment untuk template yang di-port dari Flask (mis. integrations.html)."""
from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        "static": static,
        "url": reverse,
    })
    return env

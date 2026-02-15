"""
Django template filters for markdown rendering.
"""

from django import template
from core.markdown_utils import markdown_to_html, strip_markdown

register = template.Library()


@register.filter
def markdown(text):
    """
    Convert markdown text to HTML.
    Usage in templates: {{ text|markdown }}
    """
    return markdown_to_html(text)


@register.filter
def plaintext(text):
    """
    Strip markdown formatting from text.
    Usage in templates: {{ text|plaintext }}
    """
    return strip_markdown(text)


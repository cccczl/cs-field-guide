"""Module for the custom read_file template tag."""

import os.path
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def read_static_file(filepath):
    """Read file and return contents.

    This tag should not be used on any files provided
    by users, as they contents are automatically marked
    as safe.

    Args:
        filepath (str): File to read.

    Returns:
        Contents of file.
    """
    filepath = settings.STATIC_ROOT + filepath

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f'No static file found: {filepath}')
    with open(filepath) as file_obj:
        contents = mark_safe(file_obj.read())
    return contents

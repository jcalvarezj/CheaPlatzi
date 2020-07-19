"""
This module contains common functions that other modules use
"""
import sys
import urllib.parse


def get_uri(path):
    """
    Returns normalized file URI path according to operating system
    """
    if sys.platform.startswith('win'):
        base = path.replace('\\', '/')
        return f'file:///{urllib.parse.quote(base, safe = ":/")}'
    else:
        return f'file://{urllib.parse.quote(path, safe = ":/")}'
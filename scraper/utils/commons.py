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

def validate_sku(sku):
    """
    Validates if SKU has 12 digits, if nots deletes first digit which is
    the most common digit to be added within the ecommerce
    The input should be string and the output is an integer
    """

    if (len(sku) > 12):
        cleaned_sku = sku[1:]
    else:
        cleaned_sku = sku
    
    return int(cleaned_sku)
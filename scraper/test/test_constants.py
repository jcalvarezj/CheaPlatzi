"""
This module holds the scraper's configuration constants
"""
from enum import Enum


class MockOLXConfig(Enum):
    TEST_PRODUCTS = [
        {
            'name': 'Xbox One S'#,
            # 'description': "here description",
            # 'price': "$$$",
            # 'image': "url to image",
            # 'url': "url to offer post"
        },
        {
            'name': 'PlayStation 4'#,
            # 'description': "here description",
            # 'price': "$$$",
            # 'image': "url to image",
            # 'url': "url to offer post"
        },
        {
            'name': 'Nintendo Switch'#,
            # 'description': "here description",
            # 'price': "$$$",
            # 'image': "url to image",
            # 'url': "url to offer post"
        }
    ]

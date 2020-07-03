"""
This module holds the scraper's configuration constants
"""
import os
from enum import Enum


HEADERS = {
    'Content-Type': 'application/json'
}


class MercadoLibreConfig(Enum):
    BASE_URL = 'https://api.mercadolibre.com'
    SITES_URL = f'{BASE_URL}/sites'
    BASE_SITE_URL = f'{BASE_URL}/sites/$SITE_ID'
    CATEGORIES_URL = f'{BASE_SITE_URL}/categories'
    PRODUCTS_URL = f'{BASE_SITE_URL}/search?category=$CATEGORY_ID'    
    COUNTRY_NAME = 'Colombia'
    CATEGORY_NAME = 'Consolas y Videojuegos'
    EXPORT_FILE_PATH = 'export/ml_items.json'


class OLXConfig(Enum):
    BASE_URL = 'https://www.olx.com.co/'
    PRODUCTS_URL = 'https://www.olx.com.co/video-juegos-consolas_c1022'
    SPIDER_NAME = 'olxspider'
    BASE_DOMAIN = 'olx.com.co'
    EXPORT_FILE_PATH = 'export/olx_items.json'
    RIGHT_SECT_CLASS = '_2wMiF'
    LEFT_SECT_CLASS = 'CBG3s'
    TEST_PATH = f'{os.getcwd()}/scraper/test/olx_mocks'
    TEST_PRODUCTS = [
        {
            'name': 'Xbox One S',
            'description': "here description"#,
            # 'price': "$$$",
            # 'image': "url to image",
            # 'url': "url to offer post"
        },
        {
            'name': 'PlayStation 4',
            'description': "here description"#,
            # 'price': "$$$",
            # 'image': "url to image",
            # 'url': "url to offer post"
        },
        {
            'name': 'Nintendo Switch',
            'description': "here description"#,
            # 'price': "$$$",
            # 'image': "url to image",
            # 'url': "url to offer post"
        }
    ]
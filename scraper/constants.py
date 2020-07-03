"""
This module holds the scraper's configuration constants
"""
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
    TEST_PRODUCTS = [
        {
            'name': Xbox One S#,
            # 'description': "product_name",
            # 'price': "asdf",
            # 'image': "aaaaa",
            # 'url': "Encontradas 20 cajas"
        },
        {
            'name': PlayStation 4#,
            # 'description': "product_name",
            # 'price': "asdf",
            # 'image': "aaaaa",
            # 'url': "Encontradas 20 cajas"
        },
        {
            'name': Nintendo Switch#,
            # 'description': "product_name",
            # 'price': "asdf",
            # 'image': "aaaaa",
            # 'url': "Encontradas 20 cajas"
        }
    ]


class OLXConfig(Enum):
    BASE_URL = 'https://www.olx.com.co/'
    SPIDER_NAME = 'olxspider'
    BASE_DOMAIN = 'olx.com.co'
    EXPORT_FILE_PATH = 'export/olx_items.json'

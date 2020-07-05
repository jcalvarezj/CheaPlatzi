"""
This module holds the scraper's configuration constants
"""
import os
import urllib.parse
from enum import Enum


def _get_test_products(path, html_desc = False):
    """
    Creates a list of test products
    """
    EXPECTED_DESCS = [
        'Ultima consola de Nintendo. Con controles extra.',
        'Completamente nuevo. Color blanco. 33 juegos.',
        'Consola de Microsoft con 7 juegos.'
    ]
    return [
        {
            'name': 'Nintendo Switch',
            'description': EXPECTED_DESCS[0] if not html_desc
                           else f'<p>{EXPECTED_DESCS[0]}</p>',
            'price': '$ 1.000.000',
            'image': urllib.parse.quote(f'file:///{path}/switch.jpg',
                                        safe = '/:'),
            'url': urllib.parse.quote(f'file:///{path}/switch_mock.html',
                                      safe = '/:')
        },
        {
            'name': 'PlayStation 4',
            'description': EXPECTED_DESCS[1] if not html_desc
                           else f'<p>{EXPECTED_DESCS[1]}</p>',
            'price': '$ 1.350.000',
            'image': urllib.parse.quote(f'file:///{path}/play.jpg',
                                        safe = '/:'),
            'url': urllib.parse.quote(f'file:///{path}/playstation_mock.html',
                                      safe = '/:')
        },
        {
            'name': 'Xbox One S',
            'description': EXPECTED_DESCS[2] if not html_desc
                           else f'<p>{EXPECTED_DESCS[2]}</p>',
            'price': '$ 1.550.000',
            'image': urllib.parse.quote(f'file:///{path}/xbox.jpg',
                                        safe = '/:'),
            'url': urllib.parse.quote(f'file:///{path}/xbox_mock.html',
                                      safe = '/:')
        }
    ]


HEADERS = {
    'Content-Type': 'application/json'
}


class MercadoLibreConfig(Enum):
    """
    This enum provides configuration constants for MercadoLibre scraping
    """
    BASE_URL = 'https://api.mercadolibre.com'
    SITES_URL = f'{BASE_URL}/sites'
    BASE_SITE_URL = f'{BASE_URL}/sites/$SITE_ID'
    CATEGORIES_URL = f'{BASE_SITE_URL}/categories'
    PRODUCTS_URL = f'{BASE_SITE_URL}/search?category=$CATEGORY_ID'    
    COUNTRY_NAME = 'Colombia'
    CATEGORY_NAME = 'Consolas y Videojuegos'
    EXPORT_FILE_PATH = 'export/ml_items.json'


class OLXConfig(Enum):
    """
    This enum provides configuration constants for OLX scraping
    """
    PRODUCTS_URL = 'https://www.olx.com.co/video-juegos-consolas_c1022'
    SPIDER_NAME = 'olxspider'
    ITEM_CLASS = 'itemBox'
    EXPORT_FILE_PATH = 'export/olx_items.json'
    RIGHT_SECT_CLASS = '_2wMiF'
    LEFT_SECT_CLASS = 'CBG3S'
    IMG_DIV_CLASS = 'slick-active'
    TEST_PATH = f'{os.getcwd()}/scraper/test/olx_mocks'
    TEST_FILE = 'olx_mock.html'
    TEST_PRODUCTS = _get_test_products(TEST_PATH)


class ColombiaGamerConfig(Enum):
    """
    This enum provides configuration constants for ColombiaGamer scraping
    """
    PRODUCT_URLS = [
        'https://www.colombiagamer.com.co/productos/xbox-one',
        'https://www.colombiagamer.com.co/productos/playstation-4',
        'https://www.colombiagamer.com.co/productos/nintendo-switch'
    ]
    SPIDER_NAME = 'cgamerspider'
    EXPORT_FILE_PATH = 'export/cgamer_items.json'
    ITEM_CLASS = 'product-container'
    IMG_CLASS = 'main-image'
    TITLE_CLASS = 'vm-product-title'
    PRICE_CLASS = 'PricesalesPrice'
    DESC_CLASS = 'product-description'
    TEST_PATH = f'{os.getcwd()}/scraper/test/cgamer_mocks'
    TEST_FILES = ['cgamer_switch_mock.html', 'cgamer_playstation_mock.html',
                  'cgamer_xbox_mock.html']
    TEST_PRODUCTS = _get_test_products(TEST_PATH, True)
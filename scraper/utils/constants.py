"""
This module holds the scraper's configuration constants
"""
import os
import urllib.parse
from enum import Enum


def _get_test_products(path):
    """
    Creates a list of test products
    """
    return [
        {
            'name': 'Nintendo Switch',
            # 'description': 'Ultima consola de Nintendo. Con controles extra.',
            'price': '$ 1.000.000',
            'image': urllib.parse.quote(f'file:///{path}/switch.jpg', safe = '/:')#,
            # 'url': urllib.parse.quote(f'file:///{path}/switch_mock.html', safe = '/:')
        },
        {
            'name': 'PlayStation 4',
            # 'description': 'Completamente nuevo. Color blanco. 33 juegos.',
            'price': '$ 1.350.000',
            'image': urllib.parse.quote(f'file:///{path}/play.jpg', safe = '/:')#,
            # 'url': urllib.parse.quote(f'file:///{path}/playstation_mock.html', safe = '/:')
        },
        {
            'name': 'Xbox One S',
            # 'description': 'Consola de Microsoft con 7 juegos.',
            'price': '$ 1.550.000',
            'image': urllib.parse.quote(f'file:///{path}/xbox.jpg', safe = '/:')#,
            # 'url': urllib.parse.quote(f'file:///{path}/xbox_mock.html', safe = '/:')
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
    PRODUCTS_URL = f'https://www.olx.com.co/video-juegos-consolas_c1022'
    SPIDER_NAME = 'olxspider'
    EXPORT_FILE_PATH = 'export/olx_items.json'
    RIGHT_SECT_CLASS = '_2wMiF'
    LEFT_SECT_CLASS = 'CBG3S'
    IMG_DIV_CLASS = 'slick-active'
    TEST_PATH = f'{os.getcwd()}/scraper/test/olx_mocks'
    TEST_FILE = 'olx_mock.html'
    TEST_PRODUCTS = _get_test_products(TEST_PATH)


class ExitoConfig(Enum):
    """
    This enum provides configuration constants for Exito scraping
    """
    PRODUCTS_URL = 'https://www.exito.com/tecnologia/consolas-y-videojuegos'
    SPIDER_NAME = 'exitospider'
    EXPORT_FILE_PATH = 'export/exito_items.json'
    ITEM_CLASS = 'vtex-product-summary-2-x-container'
    NAME_CLASS = 'vtex-store-components-3-x-productBrand'
    PRICE_CLASS = 'product-detail-exito-vtex-components-selling-price'
    IMAGE_CLASS = 'vtex-store-components-3-x-productImageTag'
    DESC_CLASS = 'exito-product-details-3-x-productDescriptionText'
    TEST_PATH = f'{os.getcwd()}/scraper/test/exito_mocks'
    TEST_FILE = 'exito_mock.html'
    TEST_PRODUCTS = _get_test_products(TEST_PATH)
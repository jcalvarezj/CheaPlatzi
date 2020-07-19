"""
This module holds the scraper's configuration constants
"""
import os
import sys
import urllib.parse
from enum import Enum
from .commons import get_uri

HEADERS = {
    'Content-Type': 'application/json'
}
SITE_IDS = {
    'MercadoLibre': 1,
    'ColombiaGamer': 2,
    'OLX': 3,
    'GamePlanet': 4,
    'Sears': 5,
    'MixUp': 6
}
BRAND_IDS = {
    'nintendo': 1,
    'xbox': 2,
    'playstation': 3
}
BACKEND_URL = 'https://cheaplatzi.uc.r.appspot.com/api/product'


def _get_test_products(path, site_id, html_desc = False, short_desc = False):
    """
    Creates a list of test products with the specified test path. The html_desc
    parameter indicates whether the expected description is plain text or HTML
    """    
    EXPECTED_DESCS = [
        'Ultima consola de Nintendo. Con controles extra.',
        'Completamente nuevo. Color blanco. 33 juegos.',
        'Consola de Microsoft con 7 juegos.'
    ]
    return [
        {
            'id_ecommerce': site_id,
            'id_type_product': BRAND_IDS['nintendo'],
            'name': 'Nintendo Switch',
            'description': EXPECTED_DESCS[0] if not html_desc
                           else f'<p>{EXPECTED_DESCS[0]}</p>' if not short_desc
                               else f'<p>Short</p>\n<p>{EXPECTED_DESCS[0]}</p>',
            'price': 1000000,
            'image': f'{get_uri(path)}/switch.jpg',
            'url': f'{get_uri(path)}/switch_mock.html',
            'barcode': 12345
        },
        {
            'id_ecommerce': site_id,
            'id_type_product': BRAND_IDS['playstation'],
            'name': 'PlayStation 4',
            'description': EXPECTED_DESCS[1] if not html_desc
                           else f'<p>{EXPECTED_DESCS[1]}</p>' if not short_desc
                               else f'<p>Short</p>\n<p>{EXPECTED_DESCS[1]}</p>',
            'price': 1350000,
            'image': f'{get_uri(path)}/play.jpg',
            'url': f'{get_uri(path)}/playstation_mock.html',
            'barcode': 12346
        },
        {
            'id_ecommerce': site_id,
            'id_type_product': BRAND_IDS['xbox'],
            'name': 'Xbox One S',
            'description': EXPECTED_DESCS[2] if not html_desc
                           else f'<p>{EXPECTED_DESCS[2]}</p>' if not short_desc
                               else f'<p>Short</p>\n<p>{EXPECTED_DESCS[2]}</p>',
            'price': 1550000,
            'image': f'{get_uri(path)}/xbox.jpg',
            'url': f'{get_uri(path)}/xbox_mock.html',
            'barcode': 12347
        }
    ]


class MercadoLibreConfig(Enum):
    """
    This enum provides configuration constants for MercadoLibre scraping
    """
    BASE_URL = 'https://api.mercadolibre.com'
    COUNTRY_ID = 'MCO'
    CATEGORY_ID = 'MCO1144'
    PRODUCT_ID_PARAM = '$PRODUCT_ID'
    BASE_SITE_URL = f'{BASE_URL}/sites/{COUNTRY_ID}'
    SEARCH_URL = f'{BASE_SITE_URL}/search'
    PRODUCT_URLS = [
        f'{SEARCH_URL}?q=nintendo%20switch',
        f'{SEARCH_URL}?q=ps4',
        f'{SEARCH_URL}?q=xbox%20one'
    ]
    DETAIL_URL = f'{BASE_URL}/items/{PRODUCT_ID_PARAM}'
    DESC_URL = f'{DETAIL_URL}/description'
    TEST_XBOX_ID = 'MCO12347'
    TEST_PS4_ID = 'MCO12346'
    TEST_SWITCH_ID = 'MCO12345'
    TEST_INDEX_URLS = list(map(lambda url: f'{url}&offset=0&limit=0',
                           PRODUCT_URLS))
    TEST_DESCRIPTION_URLS = [
        DESC_URL.replace(PRODUCT_ID_PARAM, TEST_SWITCH_ID),
        DESC_URL.replace(PRODUCT_ID_PARAM, TEST_PS4_ID),
        DESC_URL.replace(PRODUCT_ID_PARAM, TEST_XBOX_ID)
    ]
    TEST_PRODUCT_URLS = [
        DETAIL_URL.replace(PRODUCT_ID_PARAM, TEST_SWITCH_ID),
        DETAIL_URL.replace(PRODUCT_ID_PARAM, TEST_PS4_ID),
        DETAIL_URL.replace(PRODUCT_ID_PARAM, TEST_XBOX_ID)
    ]
    TEST_PATH_RELATIVE = 'scraper/test/mercadolibre_mocks'
    TEST_PATH = f'{os.getcwd()}/{TEST_PATH_RELATIVE}'
    TEST_INDEX_FILES = [
        'switch_index_base.json',
        'playstation_index_base.json',
        'xbox_index_base.json'
    ]
    TEST_INDEX_FILES_PARSED = [
        'switch_index.json',
        'playstation_index.json',
        'xbox_index.json'
    ]
    TEST_DESCRIPTION_FILES = [
        'switch_description.json',
        'playstation_description.json',
        'xbox_description.json'
    ]
    TEST_PRODUCT_FILES = [
        'switch_product_base.json',
        'playstation_product_base.json',
        'xbox_product_base.json'
    ]
    TEST_PRODUCT_FILES_PARSED = [
        'switch_product.json',
        'playstation_product.json',
        'xbox_product.json'
    ]
    TEST_PRODUCTS = _get_test_products(TEST_PATH, SITE_IDS['MercadoLibre'])
    EXPORT_FILE_PATH = 'export/ml_items.json'
    DELAY_IN_SECS = 1
    MAX_OFFSET = 1000
    LIMIT = 20


class OLXConfig(Enum):
    """
    This enum provides configuration constants for OLX scraping
    """
    BASE_URL = 'https://www.olx.com.co/video-juegos-consolas_c1022'
    PRODUCT_URLS = [
        f'{BASE_URL}/q-xbox-one',
        f'{BASE_URL}/q-ps4',
        f'{BASE_URL}/q-switch'
    ]
    SPIDER_NAME = 'olxspider'
    DRIVER_TIMEOUT = 3#0
    DELAY_IN_SECS = 3
    BTN_CLASS = 'btnLoadMore'
    ITEM_CLASS = 'itemBox'
    EXPORT_FILE_PATH = 'export/olx_items.json'
    RIGHT_SECT_CLASS = '_2wMiF'
    LEFT_SECT_CLASS = 'CBG3S'
    ID_CLASS = 'fr4Cy'
    IMG_DIV_CLASS = 'slick-active'
    TEST_PATH = f'{os.getcwd()}/scraper/test/olx_mocks'
    TEST_FILES = [
        'olx_switch_mock-12345.html',
        'olx_playstation_mock12346.html',
        'olx_xbox_mock12347.html'
    ]
    TEST_PRODUCTS = _get_test_products(TEST_PATH, SITE_IDS['OLX'])


class ColombiaGamerConfig(Enum):
    """
    This enum provides configuration constants for ColombiaGamer scraping
    """
    PRODUCT_URLS = [
        'https://www.colombiagamer.com.co/productos/xbox-one',
        'https://www.colombiagamer.com.co/productos/playstation-4',
        'https://www.colombiagamer.com.co/productos/nintendo-switch?limit=24'
    ]
    SPIDER_NAME = 'cgamerspider'
    EXPORT_FILE_PATH = 'export/cgamer_items.json'
    ITEM_CLASS = 'product-container'
    IMG_CLASS = 'main-image'
    TITLE_CLASS = 'vm-product-title'
    PRICE_CLASS = 'PricesalesPrice'
    SHORT_DESC_CLASS = 'product-short-description'
    DESC_CLASS = 'product-description'
    TEST_PATH = f'{os.getcwd()}/scraper/test/cgamer_mocks'
    TEST_FILES = ['cgamer_switch_mock.html', 'cgamer_playstation_mock.html',
                  'cgamer_xbox_mock.html']
    TEST_PRODUCTS = _get_test_products(TEST_PATH, SITE_IDS['ColombiaGamer'],
                                       True, True)

    
class GamePlanetConfig(Enum):
    """
    This enum provides configuration constants for GamePlanet scraping
    """
    BASE_URL = 'https://gameplanet.com/catalogo/video-juegos'
    HW_RES = '/hardware.html?dir=desc&mostrar_inventario=652&order=popularidad'
    SW_RES = '/software.html?dir=desc&mostrar_inventario=652&order=popularidad'
    PRODUCT_URLS = [
        f'{BASE_URL}{HW_RES}&plataforma=660&mode=grid',
        f'{BASE_URL}{HW_RES}&plataforma=667&mode=grid',
        f'{BASE_URL}{HW_RES}&plataforma=671&mode=grid',
        f'{BASE_URL}{SW_RES}&plataforma=660&mode=grid',
        f'{BASE_URL}{SW_RES}&plataforma=667&mode=grid',
        f'{BASE_URL}{SW_RES}&plataforma=671&mode=grid',
    ]
    SPIDER_NAME = 'gameplspider'
    EXPORT_FILE_PATH = 'export/gamepl_items.json'
    ITEM_CLASS = 'catalog-products-new'
    TITLE_CLASS = 'h1title'
    DESC_CLASS = 'std'
    PRICE_CLASS = 'domicilio-price'
    IMAGE_ID = 'main_image'
    TAG_CLASS = 'plataforma-text'
    TEST_PATH = f'{os.getcwd()}/scraper/test/gameplanet_mocks'
    TEST_FILES = ['gameplanet_mock.html']
    TEST_PRODUCTS = _get_test_products(TEST_PATH, SITE_IDS['GamePlanet'])


class MixUpConfig(Enum):
    """
    This enum provides configuration constants for MixUp scraping
    """
    BASE_URL = 'https://www.mixup.com.mx/mixup/Productos.aspx'
    PRODUCT_URLS = [
        f'{BASE_URL}?etq=GAMNIN&etqP=GAM&bf=',
        f'{BASE_URL}?etq=GAMPS&etqP=GAM&bf=',
        f'{BASE_URL}?etq=GAMXBOX&etqP=GAM&bf=',
        f'{BASE_URL}?etq=GAMCON&etqP=GAM&bf='
    ]
    SPIDER_NAME = 'mixupspider'
    EXPORT_FILE_PATH = 'export/mixup_items.json'
    ITEM_CLASS_1 = 'item'
    ITEM_CLASS_2 = 'cover'
    TITLE_CLASS = 'megatitulo'
    DESC_CLASS = 'resenia'
    PRICE_CLASS = 'preciolista'
    IMAGE_ID = 'imgProd'
    TEST_PATH = f'{os.getcwd()}/scraper/test/mixup_mocks'
    TEST_FILES = ['mixup_mock.html']
    TEST_PRODUCTS = _get_test_products(TEST_PATH, SITE_IDS['MixUp'])


class SearsConfig(Enum):
    """
    This enum provides configuration constants for Sears scraping
    """
    PRODUCT_URLS = [
        'https://www.sears.com.mx/categoria/16659/xbox/',
        'https://www.sears.com.mx/categoria/16667/playstation/',
        'https://www.sears.com.mx/categoria/16663/nintendo/',
    ]
    SPIDER_NAME = 'searspider'
    EXPORT_FILE_PATH = 'export/sears_items.json'
    ITEM_CLASS = 'vistaRapida'
    LINK_CLASS = 'linkProducto'
    TITLE_CLASS = 'productMainContainer'
    DESC_CLASS = 'yotpo'
    PRICE_CLASS = 'total'
    IMAGE_CLASS = 'carrusel-producto'
    TEST_PATH = f'{os.getcwd()}/scraper/test/sears_mocks'
    TEST_FILES = ['sears_mock.html']
    TEST_PRODUCTS = _get_test_products(TEST_PATH, SITE_IDS['Sears'])

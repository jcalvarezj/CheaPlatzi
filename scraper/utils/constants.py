"""
This module holds the scraper's configuration constants
"""
import os
import sys
import urllib.parse
from enum import Enum


HEADERS = {
    'Content-Type': 'application/json'
}
SITE_IDS = {
    'MercadoLibre': 1,
    'ColombiaGamer': 2,
    'OLX': 3
}
BACKEND_URL = 'https://cheaplatzi.uc.r.appspot.com/api/product'


def _get_test_products(path, site_id, html_desc = False, short_desc = False):
    """
    Creates a list of test products with the specified test path. The html_desc
    parameter indicates whether the expected description is plain text or HTML
    """
    PROTOCOL = 'file:///' if sys.platform.startswith('win') else 'file://'
    EXPECTED_DESCS = [
        'Ultima consola de Nintendo. Con controles extra.',
        'Completamente nuevo. Color blanco. 33 juegos.',
        'Consola de Microsoft con 7 juegos.'
    ]
    return [
        {
            'id_ecommerce': site_id,
            'id_type_product': None,
            'name': 'Nintendo Switch',
            'description': EXPECTED_DESCS[0] if not html_desc
                           else f'<p>{EXPECTED_DESCS[0]}</p>' if not short_desc
                               else f'<p>Short</p>\n<p>{EXPECTED_DESCS[0]}</p>',
            'price': 1000000,
            'image': urllib.parse.quote(f'{PROTOCOL}{path}/switch.jpg',
                                        safe = '/:'),
            'url': urllib.parse.quote(f'{PROTOCOL}{path}/switch_mock.html',
                                      safe = '/:')
        },
        {
            'id_ecommerce': site_id,
            'id_type_product': None,
            'name': 'PlayStation 4',
            'description': EXPECTED_DESCS[1] if not html_desc
                           else f'<p>{EXPECTED_DESCS[1]}</p>' if not short_desc
                               else f'<p>Short</p>\n<p>{EXPECTED_DESCS[1]}</p>',
            'price': 1350000,
            'image': urllib.parse.quote(f'{PROTOCOL}{path}/play.jpg',
                                        safe = '/:'),
            'url': urllib.parse.quote(f'{PROTOCOL}{path}/playstation_mock.html',
                                      safe = '/:')
        },
        {
            'id_ecommerce': site_id,
            'id_type_product': None,
            'name': 'Xbox One S',
            'description': EXPECTED_DESCS[2] if not html_desc
                           else f'<p>{EXPECTED_DESCS[2]}</p>' if not short_desc
                               else f'<p>Short</p>\n<p>{EXPECTED_DESCS[2]}</p>',
            'price': 1550000,
            'image': urllib.parse.quote(f'{PROTOCOL}{path}/xbox.jpg',
                                        safe = '/:'),
            'url': urllib.parse.quote(f'{PROTOCOL}{path}/xbox_mock.html',
                                      safe = '/:')
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
    PRODUCTS_URL = f'{BASE_SITE_URL}/search?category={CATEGORY_ID}'
    DETAIL_URL = f'{BASE_URL}/items/{PRODUCT_ID_PARAM}'
    DESC_URL = f'{DETAIL_URL}/description'
    EXPORT_FILE_PATH = 'export/ml_items.json'
    DELAY_IN_SECS = 1
    MAX_OFFSET = 1000
    LIMIT = 20


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
<<<<<<< HEAD
    TEST_PRODUCTS = _get_test_products(TEST_PATH, True)

    
class GamePlanetConfig(Enum):
    """
    This enum provides configuration constants for GamePlanet scraping
    """
    PRODUCT_URLS = [
        f'https://gameplanet.com/catalogo/video-juegos/hardware.html?dir=desc&mostrar_inventario=652&order=popularidad&plataforma=660&mode=grid',
        f'https://gameplanet.com/catalogo/video-juegos/hardware.html?dir=desc&mostrar_inventario=652&order=popularidad&plataforma=667&mode=grid',
        f'https://gameplanet.com/catalogo/video-juegos/hardware.html?dir=desc&mostrar_inventario=652&order=popularidad&plataforma=671&mode=grid',
        f'https://gameplanet.com/catalogo/video-juegos/software.html?dir=desc&mostrar_inventario=652&order=popularidad&plataforma=660&mode=grid',
        f'https://gameplanet.com/catalogo/video-juegos/software.html?dir=desc&mostrar_inventario=652&order=popularidad&plataforma=667&mode=grid',
        f'https://gameplanet.com/catalogo/video-juegos/software.html?dir=desc&mostrar_inventario=652&order=popularidad&plataforma=671&mode=grid',
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
    TEST_PRODUCTS = _get_test_products(TEST_PATH)

class MixUpConfig(Enum):
    """
    This enum provides configuration constants for GamePlanet scraping
    """
    PRODUCT_URLS = [
        'https://www.mixup.com.mx/mixup/Productos.aspx?etq=GAMNIN&etqP=GAM&bf=',
        'https://www.mixup.com.mx/mixup/Productos.aspx?etq=GAMPS&etqP=GAM&bf=',
        'https://www.mixup.com.mx/mixup/Productos.aspx?etq=GAMXBOX&etqP=GAM&bf=',
        'https://www.mixup.com.mx/mixup/Productos.aspx?etq=GAMCON&etqP=GAM&bf='
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
    TEST_PRODUCTS = _get_test_products(TEST_PATH)

class SearsConfig(Enum):
    """
    This enum provides configuration constants for GamePlanet scraping
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
    TEST_PRODUCTS = _get_test_products(TEST_PATH)

=======
    TEST_PRODUCTS = _get_test_products(TEST_PATH, SITE_IDS['ColombiaGamer'],
                                       True, True)
>>>>>>> 91d3d0781653bcc0544c02fd87932d1fc8909080

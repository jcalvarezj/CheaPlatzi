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
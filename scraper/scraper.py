"""
This module is in charge of performing requests to e-commerce sites' public 
APIs, in order to retrieve product data
"""

import grequests


TEST_COUNTRY_ID = 'MCO'
HEADERS = {
    'Content-Type': 'application/json'
}
BASE_URL = 'https://api.mercadolibre.com'
SITES_URL = f'{BASE_URL}/sites'
BASE_SITE_URL = f'{BASE_URL}/sites/$SITE_ID'
CATEGORIES_URL = f'{BASE_SITE_URL}/categories'
PRODUCTS_URL = f'{BASE_SITE_URL}/search?category=$CATEGORY_ID'
COUNTRY_NAME = 'Colombia'
CATEGORY_NAME = 'Consolas y Videojuegos'


def handle_exception(request, exception):
    """
    Exception handler callback function
    """
    print('Could not perform the request due to a problem:')
    print(exception)


def send_request(endpoints, country_id = "", category_id = ""):
    """
    Attempts to send a request with for the specified list of endpoints.
    If the endpoints have $SITE_ID and $CATEGORY_ID URL parameters, the 
    country_id and category_id parameters are respectively required

    This method returns a list of response objects
    """
    pending_requests = []

    for endpoint in endpoints:
        parsed_endpoint = endpoint.replace('$SITE_ID', country_id) \
                              .replace('$CATEGORY_ID', category_id)

        pending_requests.append(grequests.get(parsed_endpoint,
                                              headers = HEADERS))

    responses = grequests.map(pending_requests,
                              exception_handler = handle_exception)

    for index, response in enumerate(responses):
        r_url = response.request.url

        if (response.status_code == 200):
            print(f'\n{"*" * 70}')
            print(f'SUCCESS! Response #{index} for {r_url}:\n')
            print(response.json())
            print(f'{"*" * 70}\n')
        else:
            print(f'\n{"*" * 70}')
            print(f'Problem with the request to {r_url}. ')
            print(f'Response #{index}:')
            print(response.status_code)
            print(response.json())
            print(f'{"*" * 70}\n')

    return responses


def _find_exact_among_records(records_collection, match, prop):
    """
    Retrieves the first find with exactly the specified mathching string for a
    specified property (prop), within a collection of dictionary/json records
    """
    return next((record for record in records_collection
                if record[prop].strip() == match), None)


def _find_contains_among_records(records_collection, match, prop):
    """
    Retrieves all the finds with the specified mathching string contained in a
    specified property (prop), within a collection of dictionary/json records
    """
    return [record for record in records_collection
            if match.upper() in record[prop].upper()]


if __name__ == "__main__":
    print(f'Trying to get {COUNTRY_NAME}\'s id')

    country_responses = send_request([SITES_URL])
    countries = country_responses[0].json()

    found_country = _find_exact_among_records(countries, COUNTRY_NAME, 'name')
    country_id = found_country['id']

    print(f'{COUNTRY_NAME}\'s id is {country_id}')
    print(f'Trying to get all the categories for country id {country_id}')

    category_reponses = send_request([CATEGORIES_URL], country_id = country_id)
    categories = category_reponses[0].json()

    print(f'Trying to get the id of the "{CATEGORY_NAME}" category')

    found_category = _find_exact_among_records(categories, CATEGORY_NAME, 'name')
    category_id = found_category['id']

    print(f'"{CATEGORY_NAME}" in {COUNTRY_NAME}\'s site has id: {category_id}')
    print(f'Retrieving all products for {CATEGORY_NAME}')

    product_responses = send_request([PRODUCTS_URL], country_id, category_id)

    products = product_responses[0].json()

    print(f'{products["paging"]["total"]} items found in this category')
    print(f'The current page displays {products["paging"]["limit"]} items')

    print('Trying to find "Playstation" items\n')

    playstations = _find_contains_among_records(products['results'],
                                                'Playstation', 'title')

    print(playstations)
"""
This module contains the definiton of functions for API consuming
"""
import time
import json
import grequests
from .constants import MercadoLibreConfig as MLC
from .constants import HEADERS, SITE_IDS, BRAND_IDS


def _handle_exception(request, exception):
    """
    Exception handler callback function
    """
    print('Could not perform the request due to a problem:')
    print(exception)


def parse_endpoint(endpoint, params_dict):
    """
    Returns the endpoint with values parameters replaced with their values
    """
    parsed_endpoint = endpoint

    for param, value in params_dict.items():
        parsed_endpoint = parsed_endpoint.replace(param, value)

    return parsed_endpoint


def _print_response_success(response, index, expected_code, verbose):
    """
    Prints an output according to the response's status, and its json contents
    if verbose mode is enabled
    """
    request_url = response.request.url

    if response.status_code == expected_code:
        print(f'\n{"*" * 70}')
        print(f'SUCCESS! Obtained response #{index} for {request_url}\n')
        if verbose:
            print(response.json())
        print(f'{"*" * 70}\n')
    else:
        print(f'\n{"*" * 70}')
        print(f'Problem with the request to {request_url}. ')
        print(f'Response #{index}:')
        print(response.status_code)
        if verbose:
            print(response.json())
        print(f'{"*" * 70}\n')


def scrap_request(endpoints, params_dict = {}, verbose = False):
    """
    Attempts to send a GET request with for the specified list of endpoints for
    scraping
    
    The params_dict parameter is a dictionary of URL parameters to replace with
    values. The verbose flag enables showing the whole response contents (json)

    This method returns a list of response objects
    """
    pending_requests = []

    for endpoint in endpoints:
        parsed_endpoint = parse_endpoint(endpoint, params_dict)

        pending_requests.append(grequests.get(parsed_endpoint,
                                              headers = HEADERS))

    responses = grequests.map(pending_requests,
                              exception_handler = _handle_exception)

    for i, response in enumerate(responses):
        if response != None:
            _print_response_success(response, i, 200, verbose)

    return responses


def store_request(page_list, endpoint, verbose):
    """
    Attempts to send multiple asynchronous POST requests to the specified
    endpoint, one for each element of the page list
    """
    pending_requests = []

    for page_data in page_list:
        pending_requests.append(grequests.post(endpoint, data = page_data,
                                               headers = HEADERS))    
    responses = grequests.map(pending_requests, 
                              exception_handler = _handle_exception)
    
    for i, response in enumerate(responses):
        if response != None:
            _print_response_success(response, i, 201, verbose)


def _get_all_mercadolibre_urls(product_index_url, limit):
    """
    Generates a list of MercadoLibre product URLs for scraping (according to
    item offsets within a specified limit)
    """
    urls = []

    N = 1

    if limit:
        N = MLC.MAX_OFFSET.value // limit + 1

    for coef in range(0, N):
        params = f'&offset={coef * limit}&limit={limit}'
        urls.append(f'{product_index_url}{params}')

    return urls


def _scrap_mercadolibre_product_pages(product_responses, brand_id, verbose):
    """
    Scraps MercadoLibre's product pages from the passed responses
    """
    records = []
        
    for i, product_response in enumerate(product_responses):
        if product_response:
            products = product_response.json()['results']

            for product in products:
                params = { MLC.PRODUCT_ID_PARAM.value: product['id'] }

                description_responses = scrap_request([MLC.DESC_URL.value],
                                                        params, verbose)

                time.sleep(MLC.DELAY_IN_SECS.value)

                img_responses = scrap_request([MLC.DETAIL_URL.value], params,
                                                verbose)

                time.sleep(MLC.DELAY_IN_SECS.value)

                description = ''
                if description_responses:
                    try:
                        description = description_responses[0].json()['plain_text']
                    except Exception:
                        print('Problem retrieving the product\'s description')

                image = ''
                barcode = ''
                if img_responses:
                    try:
                        image = img_responses[0].json()['pictures'][0]['secure_url']
                        barcode = img_responses[0].json()['id'].replace('MCO', '')
                    except Exception:
                        print('Problem retrieving the product\'s details')

                records.append({
                    'id_ecommerce': SITE_IDS['MercadoLibre'],
                    'id_type_product': brand_id,
                    'name': product['title'],
                    'description': description,
                    'price': product['price'],
                    'image': image,
                    'url': product['permalink'],
                    'barcode': int(barcode)
                })

                time.sleep(MLC.DELAY_IN_SECS.value)
        else:
            print('No response obtained')
    return records


def scrap_mercadolibre(limit = MLC.LIMIT.value, verbose = False):
    """
    Consumes MercadoLibre's API to perform scraping of products
    The limit value establishes the maximum offset for pagination
    """ 
    pages_urls = []
    
    for product_url in MLC.PRODUCT_URLS.value:
        pages_urls.extend(_get_all_mercadolibre_urls(product_url, limit))
    
    N = len(pages_urls)

    for i, url in enumerate(pages_urls):
        product_responses = []
        response = scrap_request([url], verbose = verbose)
        product_responses.append(response[0])
        time.sleep(MLC.DELAY_IN_SECS.value)

        brand = BRAND_IDS['playstation'] if 'ps4' in url \
                else BRAND_IDS['nintendo'] if 'nintendo' in url \
                    else BRAND_IDS['xbox'] if 'xbox' in url \
                        else None

        records = _scrap_mercadolibre_product_pages(product_responses, brand,
                                                    verbose)
        index = f'{i}'.zfill(3)
        file_name = MLC.EXPORT_FILE_PATH.value.replace('.json',
                                                        f'{index}.json')

        with open(file_name, 'w', encoding = 'utf-8') as export_file:
            json.dump(records, export_file, ensure_ascii = False)
        
        print(f'Scraped page {i + 1} of {N}')

    return N
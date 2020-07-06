"""
This module is in charge of performing requests to e-commerce sites' public 
APIs, in order to retrieve product data
"""
import sys
import click
import grequests
from scrapy.crawler import CrawlerProcess
from utils.spiders import OLXSpider, CGamerSpider
from utils.constants import MercadoLibreConfig as MLC, HEADERS
from utils.constants import OLXConfig as OLX, ColombiaGamerConfig as CGamer


def _handle_exception(request, exception):
    """
    Exception handler callback function
    """
    print('Could not perform the request due to a problem:')
    print(exception)


def send_request(endpoints, country_id = "", category_id = "",
                 verbose = False):
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
                              exception_handler = _handle_exception)

    for index, response in enumerate(responses):
        r_url = response.request.url

        if response.status_code == 200:
            print(f'\n{"*" * 70}')
            print(f'SUCCESS! Obtained response #{index} for {r_url}\n')
            if verbose:
                print(response.json())
            print(f'{"*" * 70}\n')
        else:
            print(f'\n{"*" * 70}')
            print(f'Problem with the request to {r_url}. ')
            print(f'Response #{index}:')
            print(response.status_code)
            if verbose:
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


@click.command()
@click.option('--site', help = 'The index of the site to scrap', type = int,
              required = True)
@click.option('--verbose', help = 'Indicate whether or not to show additional '
              'information in the output (show API responses)', default = 0)
def run(site, verbose):
    """
    This module retrieves the list of products from the Consoles and Video
    Games category within the selected e-commerce site.

    The indexes for the sites are:

    0: MercadoLibre\n
    1: [To implement]

    Windows Use: `python .\scraper\scraper.py --site=<index> [--verbose=<0|1>]`

    Linux/Unix: `python3 ./scraper/scraper.py --site=<index> [--verbose=<0|1>]`    
    """
    if site == 0:
        print(f'Trying to get {MLC.COUNTRY_NAME.value}\'s id')

        country_responses = send_request([MLC.SITES_URL.value])
        countries = country_responses[0].json()

        found_country = _find_exact_among_records(countries,
                                                  MLC.COUNTRY_NAME.value,
                                                  'name')
        country_id = found_country['id']

        print(f'{MLC.COUNTRY_NAME.value}\'s id is {country_id}')
        print(f'Trying to get all the categories for country id {country_id}')

        category_reponses = send_request([MLC.CATEGORIES_URL.value],
                                         country_id = country_id)
        categories = category_reponses[0].json()

        print(f'Trying to get the id of the "{MLC.CATEGORY_NAME.value}"'
              'category')

        found_category = _find_exact_among_records(categories,
                                                   MLC.CATEGORY_NAME.value,
                                                   'name')
        category_id = found_category['id']

        print(f'"{MLC.CATEGORY_NAME.value}" in {MLC.COUNTRY_NAME.value}\'s '
              f'site has id: {category_id}')
        print(f'Retrieving all products for {MLC.CATEGORY_NAME.value}')

        product_responses = send_request([MLC.PRODUCTS_URL.value], country_id,
                                         category_id)
        products = product_responses[0].json()

        print(f'{products["paging"]["total"]} items found in this category')
        print(f'The current page displays {products["paging"]["limit"]} items')

        print('Trying to find "Playstation" items\n')

        playstations = _find_contains_among_records(products['results'],
                                                    'Playstation', 'title')

        print(playstations)

    elif site == 1:        
        process = CrawlerProcess()
        process.crawl(OLXSpider, start_urls = [OLX.PRODUCTS_URL.value])
        process.start()
    elif site == 2:        
        process = CrawlerProcess()
        process.crawl(CGamerSpider, start_urls = CGamer.PRODUCT_URLS.value)
        process.start()
    else:
        print('Invalid option for site')


if __name__ == "__main__":
    run()
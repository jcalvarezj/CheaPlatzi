"""
This module is in charge of performing requests to e-commerce sites' public 
APIs, in order to retrieve product data
"""
import sys
import time
import json
import click
import utils.apis as apis
from scrapy.crawler import CrawlerProcess
from utils.constants import MercadoLibreConfig as MLC, BACKEND_URL, SITE_IDS
from utils.spiders import OLXSpider, ColombiaGamerSpider as CGamerSpider
from utils.constants import OLXConfig as OLX, ColombiaGamerConfig as CGamer


def _store_in_remote_database(results_path, scrap_api = False, n_pages = 0,
                              verbose = False):
    """
    This function sends the scraped data found as json files to the remote
    database through POST requests

    results_path is the base path to the file
    scrap_api indicates whether data has been scraped through an API
    n_pages indicates the number of scraped pages through an API
    """
    print('Sending requests to the backend\'s database API')

    if scrap_api:
        data = []
        for i in range(0, n_pages):
            index = f'{i}'.zfill(3)
            file_name = results_path.replace('.json', f'{index}.json')

            with open(file_name, encoding = 'utf-8') as data_file:
                data.append(json.dumps(json.load(data_file)))

        apis.store_request(data, BACKEND_URL, verbose)
    else:
        data = ""
        with open(results_path, encoding = 'utf-8') as data_file:
            data = json.dumps(json.load(data_file))

        apis.store_request([data], BACKEND_URL, verbose)

    print('Finished sending data to the backend')


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


def _get_all_mercadolibre_urls():
    """
    Generates a list of MercadoLibre product URLs for scraping (item offsets)
    """
    urls = []

    for coef in range(0, MLC.MAX_OFFSET.value // MLC.LIMIT.value + 1):
        params = f'&offset={coef * MLC.LIMIT.value}&limit={MLC.LIMIT.value}'
        urls.append(f'{MLC.PRODUCTS_URL.value}{params}')

    return urls


def _scrap_mercadolibre_product_pages(product_responses, verbose):
    """
    Scraps MercadoLibre's product pages from the passed responses
    """
    records = []
        
    for i, product_response in enumerate(product_responses):
        products = product_response.json()['results']

        print(f'Going to scrap {len(products)} items')

        for product in products:
            params = { MLC.PRODUCT_ID_PARAM.value: product['id'] }

            description_responses = apis.scrap_request([MLC.DESC_URL.value],
                                                    params, verbose)

            time.sleep(MLC.DELAY_IN_SECS.value)

            img_responses = apis.scrap_request([MLC.DETAIL_URL.value], params,
                                                verbose)

            time.sleep(MLC.DELAY_IN_SECS.value)

            description = ""
            if description_responses:
                try:
                    description = description_responses[0].json()['plain_text']
                except Exception:
                    description = "{PROBLEM OBTAINING THIS ITEM'S DESCRIPTION}"

            image = ""
            if img_responses:
                try:
                    image = img_responses[0].json()['pictures'][0]['secure_url']
                except Exception:
                    image = "{PROBLEM OBTAINING THIS ITEM'S IMAGE URL}"

            records.append({
                'id_type_product': None,
                'id_ecommerce': SITE_IDS['MercadoLibre'],
                'name': product['title'],
                'description': description,
                'price': product['price'],
                'image': image,
                'url': product['permalink']
            })

            time.sleep(MLC.DELAY_IN_SECS.value)

    return records


@click.command()
@click.option('--site', help = 'The index of the site to scrap', type = int,
              required = True)
@click.option('--verbose', help = 'If present, show additional information in '
              'the output (show full API responses)', is_flag = True)
@click.option('--store', help = 'This flag enables sending requests to the '
              'backend\'s database API to store the records', is_flag = True)
def run(site, verbose, store):
    """
    This module retrieves the list of products from the Consoles and Video
    Games category within the selected e-commerce site.

    The indexes for the sites are:

    0: MercadoLibre\n
    1: OLX\n
    2: ColombiaGamer

    Windows Use: 
    
        `python .\scraper\scraper.py --site=<index> [--verbose] [--store]`

    Linux/Unix Use:
    
        `python3 ./scraper/scraper.py --site=<index> [--verbose] [--store]`
    """
    if site == 0:
        urls = _get_all_mercadolibre_urls()
        N = MLC.MAX_OFFSET.value // MLC.LIMIT.value + 1

        for i, url in enumerate(urls):
            product_responses = []
            response = apis.scrap_request([url], verbose = verbose)
            product_responses.append(response[0])
            time.sleep(MLC.DELAY_IN_SECS.value)

            records = _scrap_mercadolibre_product_pages(product_responses,
                                                        verbose)
            index = f'{i}'.zfill(3)
            file_name = MLC.EXPORT_FILE_PATH.value.replace('.json',
                                                           f'{index}.json')

            with open(file_name, 'w', encoding = 'utf-8') as export_file:
                json.dump(records, export_file, ensure_ascii = False)
            
            print(f'Scraped page {i+1} of {N}')

        print(f'Finished scraping MercadoLibre!\n')

        if store:
            _store_in_remote_database(MLC.EXPORT_FILE_PATH.value, True, N,
                                      verbose)
    elif site == 1:
        process = CrawlerProcess()
        process.crawl(OLXSpider, start_urls = OLX.PRODUCT_URLS.value)
        process.start()

        print(f'Finished scraping OLX!\n')

        if store:
            _store_in_remote_database(OLX.EXPORT_FILE_PATH.value,
                                      verbose = verbose)
    elif site == 2:
        process = CrawlerProcess()
        process.crawl(CGamerSpider, start_urls = CGamer.PRODUCT_URLS.value)
        process.start()

        print(f'Finished scraping ColombiaGamer!\n')

        if store:
            _store_in_remote_database(CGamer.EXPORT_FILE_PATH.value,
                                      verbose = verbose)
    else:
        print('Invalid option for site')


if __name__ == "__main__":
    run()
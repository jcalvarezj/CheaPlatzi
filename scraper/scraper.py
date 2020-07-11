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
        N = apis.scrap_mercadolibre(verbose = verbose)

        print(f'Finished scraping MercadoLibre!\n')

        if store:
            _store_in_remote_database(MLC.EXPORT_FILE_PATH.value, True, N,
                                      verbose)
    elif site == 1:
        process = CrawlerProcess()
        process.crawl(OLXSpider, start_urls = [OLX.PRODUCTS_URL.value])
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
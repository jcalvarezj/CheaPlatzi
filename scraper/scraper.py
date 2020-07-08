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
from utils.constants import MercadoLibreConfig as MLC
from utils.spiders import OLXSpider, ColombiaGamerSpider as CGamerSpider, GamePlSpider
from utils.constants import OLXConfig as OLX, ColombiaGamerConfig as CGamer, GamePlanetConfig as GamePl


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
    1: OLX\n
    2: ColombiaGamer

    Windows Use: `python .\scraper\scraper.py --site=<index> [--verbose=<0|1>]`

    Linux/Unix: `python3 ./scraper/scraper.py --site=<index> [--verbose=<0|1>]`
    """
    if site == 0:
        product_responses = apis.send_request([MLC.PRODUCTS_URL.value],
                                              verbose = verbose)
        products = product_responses[0].json()['results']

        records = []

        print(f'Going to scrap {len(products)} items')

        for product in products:
            params = { MLC.PRODUCT_ID_PARAM.value: product['id'] }

            description_responses = apis.send_request([MLC.DESC_URL.value],
                                                    params, verbose)


            time.sleep(MLC.DELAY_IN_SECS.value)

            img_responses = apis.send_request([MLC.DETAIL_URL.value], params,
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
                'name': product['title'],
                'description': description,
                'price': product['price'],
                'image': image,
                'url': product['permalink']
            })

            time.sleep(MLC.DELAY_IN_SECS.value)

        with open(MLC.EXPORT_FILE_PATH.value, 'w') as export_file:
            export_file.write(json.dumps(records, indent = 4))

        print(f'Finished scraping! All results are in {MLC.EXPORT_FILE_PATH}')
    elif site == 1:
        process = CrawlerProcess()
        process.crawl(OLXSpider, start_urls = [OLX.PRODUCTS_URL.value])
        process.start()
    elif site == 2:
        process = CrawlerProcess()
        process.crawl(CGamerSpider, start_urls = CGamer.PRODUCT_URLS.value)
        process.start()
    elif site == 3:
        process = CrawlerProcess()
        process.crawl(GamePlSpider, start_urls = GamePl.PRODUCT_URLS.value)
        process.start()
    else:
        print('Invalid option for site')


if __name__ == "__main__":
    run()
"""
This module performs unit tests on the scraper module
"""
import os
import json
import pytest
from ..utils.spiders import OLXSpider, ExitoSpider
from ..utils.constants import OLXConfig as OLX, ExitoConfig as Exito
from scrapy.crawler import CrawlerProcess


def cleanup(created_file_path = None):
    """
    Deletes a file the test process created
    """
    if created_file_path:
        os.remove(created_file_path)


def olx_setup():
    """
    Initializes the required conditions for testing on OLX's site
    """
    fileURI = f'file:{OLX.TEST_PATH.value}/{OLX.TEST_FILE.value}'

    process = CrawlerProcess()
    process.crawl(OLXSpider, start_urls = [fileURI])
    process.start()


def exito_setup():
    """
    Initializes the required conditions for testing on Exito's site
    """
    fileURI = f'file:{Exito.TEST_PATH.value}/{Exito.TEST_FILE.value}'

    process = CrawlerProcess()
    process.crawl(ExitoSpider, start_urls = [fileURI])
    process.start()

## TODO: Uncomment when finished testing Exito !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# def test_olx_scrapper_happy_path_json_data_exported():
#     """
#     This test case checks if the scraper generates the right json file after
#     scraping a mock with OLX's site structure
#     """
#     olx_setup()

#     file_path = f'{OLX.EXPORT_FILE_PATH.value}'

#     assert os.path.exists(file_path), f'expected the file {file_path} to exist'

#     with open(file_path) as json_file:
#         data = json.load(json_file)
#         assert data == OLX.TEST_PRODUCTS.value, \
#                'the exported json file does not match the expected result'

#     cleanup(file_path)


def test_exito_scrapper_happy_path_json_data_exported():
    """
    This test case checks if the scraper generates the right json file after
    scraping a mock with Exito's site structure
    """
    exito_setup()

    file_path = f'{Exito.EXPORT_FILE_PATH.value}'

    assert os.path.exists(file_path), f'expected the file {file_path} to exist'

    with open(file_path) as json_file:
        data = json.load(json_file)
        assert data == Exito.TEST_PRODUCTS.value, \
               'the exported json file does not match the expected result'

    cleanup(file_path)


## TODO: test when there are no articles
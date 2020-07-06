"""
This module performs unit tests on the scraper module
"""
import os
import json
import pytest
from ..utils.spiders import OLXSpider, ColombiaGamerSpider as CGamerSpider
from ..utils.constants import OLXConfig as OLX, ColombiaGamerConfig as CGamer
from scrapy.crawler import CrawlerProcess


def cleanup(created_file_path):
    """
    Deletes a file the test process created
    """
    try:
        os.remove(created_file_path)
    except OSError:
        pass


def olx_setup():
    """
    Initializes the required conditions for testing on OLX's site
    """
    fileURI = f'file:{OLX.TEST_PATH.value}/{OLX.TEST_FILE.value}'

    process = CrawlerProcess()
    process.crawl(OLXSpider, start_urls = [fileURI])
    process.start()


def cgamer_setup():
    """
    Initializes the required conditions for testing on ColombiaGamer's site
    """
    fileURIs = [f'file:{CGamer.TEST_PATH.value}/{file_name}' for file_name 
                in CGamer.TEST_FILES.value]
    
    process = CrawlerProcess()
    process.crawl(CGamerSpider, start_urls = fileURIs)
    process.start()


def test_olx_scrapper_happy_path_json_data_exported():
    """
    This test case checks if the scraper generates the right json file after
    scraping a mock with OLX's site structure
    """
    file_path = f'{OLX.EXPORT_FILE_PATH.value}'
    cleanup(file_path)
    olx_setup()

    assert os.path.exists(file_path), f'expected the file {file_path} to exist'

    with open(file_path) as json_file:
        data = json.load(json_file)
        
        assert data == OLX.TEST_PRODUCTS.value, \
                'the exported json file does not match the expected result'

    cleanup(file_path)


def test_cgamer_scrapper_happy_path_json_data_exported():
    """
    This test case checks if the scraper generates the right json file after
    scraping a mock with CGamer's site structure
    """
    file_path = f'{CGamer.EXPORT_FILE_PATH.value}'
    cleanup(file_path)
    cgamer_setup()

    assert os.path.exists(file_path), f'expected the file {file_path} to exist'

    with open(file_path) as json_file:
        data = json.load(json_file)
        assert data == CGamer.TEST_PRODUCTS.value, \
                'the exported json file does not match the expected result'

    cleanup(file_path)
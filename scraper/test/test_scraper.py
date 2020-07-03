"""
This module performs unit tests on the scraper module
"""
import pytest
import os.path
from ..utils.spiders import OLXSpider
from ..utils.constants import OLXConfig as OLX
from scrapy.crawler import CrawlerProcess


def olx_setup():
    """
    Initializes the required conditions for testing on OLX
    """
    process = CrawlerProcess()
    process.crawl(OLXSpider, settings = {'start_urls': [OLX.PRODUCTS_URL.value]})
    process.start()


def test_olx_scrapper_happy_path_json_data_exported():
    """
    This test case checks if the scraper generates the right json file after
    scraping a mock with OLX structure
    """
    olx_setup()

    file_path = f'{OLX.EXPORT_FILE_PATH.value}'

    assert os.path.exists(file_path), f'expected the file {file_path} to exist'
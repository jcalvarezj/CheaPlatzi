"""
This module performs unit tests on the scraper module
"""
import pytest
import os.path
from ..spiders import OLXSpider
from ..constants import OLXConfig as OLX
from scrapy.crawler import CrawlerProcess


def olx_setup():
    process = CrawlerProcess()
    process.crawl(OLXSpider)
    process.start()


def test_olx_scrapper_happy_path_json_data_exported():
    """
    This test case checks if the scraper generates the right json file after
    scraping a mock with OLX structure
    """
    olx_setup()

    assert os.path.exists(f'../{OLX.EXPORT_FILE_NAME.value}'), 'expected the file to exist'
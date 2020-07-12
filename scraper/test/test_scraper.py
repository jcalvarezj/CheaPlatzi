"""
This module performs unit tests on the scraper module
"""
import os
import sys
import json
import pytest
import requests
import responses
import urllib.parse
from ..utils import apis
from ..utils.spiders import GamePlSpider, MixUpSpider, SearSpider
from ..utils.spiders import OLXSpider, ColombiaGamerSpider as CGamerSpider
from ..utils.constants import MercadoLibreConfig as MLC, SearsConfig as SEA
from ..utils.constants import OLXConfig as OLX, ColombiaGamerConfig as CGamer
from ..utils.constants import GamePlanetConfig as GamePl, MixUpConfig as MUC
from scrapy.crawler import CrawlerProcess


def _cleanup(created_file_path):
    """
    Deletes a file the test process created
    """
    try:
        os.remove(created_file_path)
    except OSError:
        pass


def _generate_mock_response_file(base_file_URIs, is_index = True):
    """
    Generates the mock response file from the base file URIs

    is_index indicates whether the files correspond to the index response
    """
    for file_URI in base_file_URIs:
        with open(file_URI, encoding = 'utf-8') as json_file:
            data = json.load(json_file)
            path = MLC.TEST_PATH.value
            PROTOCOL = 'file:///' if sys.platform.startswith('win') \
                       else 'file://'
            base_URI = urllib.parse.quote(f'{PROTOCOL}{path}', safe = '/:')

            if not is_index:
                current_image = data['pictures'][0]['secure_url']
                new_value = ''

                if current_image == '$XBOXIMAGE':
                    new_value = f'{base_URI}/xbox.jpg'
                elif current_image == '$SWITCHIMAGE':
                    new_value = f'{base_URI}/switch.jpg'
                else:
                    new_value = f'{base_URI}/play.jpg'                    

                data['pictures'][0]['secure_url'] = new_value
            else:
                current_link = data['results'][0]['permalink']
                new_value = ''

                if current_link == '$XBOXLINK':
                    new_value = f'{base_URI}/xbox_mock.html'
                elif current_link == '$SWITCHLINK':
                    new_value = f'{base_URI}/switch_mock.html'
                else:
                    new_value = f'{base_URI}/playstation_mock.html'

                data['results'][0]['permalink'] = new_value
            
            new_file_name = file_URI.replace('_base', '')

            with open(new_file_name, 'w', encoding = 'utf-8') as export_file:
                json.dump(data, export_file, ensure_ascii = False)


def _mercadolibre_setup():
    """
    Initializes the required conditions for testing on MercadoLibre's API
    """
    product_base_file_URIs = [f'{MLC.TEST_PATH.value}/{file_name}'
                         for file_name in MLC.TEST_PRODUCT_FILES.value]
    
    index_base_file_URIs = [f'{MLC.TEST_PATH.value}/{file_name}'
                      for file_name in MLC.TEST_INDEX_FILES.value]
    
    _generate_mock_response_file(index_base_file_URIs)
    _generate_mock_response_file(product_base_file_URIs, False)


def _olx_setup():
    """
    Initializes the required conditions for testing on OLX's site
    """
    fileURIs = [f'file:{OLX.TEST_PATH.value}/{file_name}' for file_name
                in OLX.TEST_FILES.value]

    process = CrawlerProcess()
    process.crawl(OLXSpider, start_urls = fileURIs)
    process.start()


def _cgamer_setup():
    """
    Initializes the required conditions for testing on ColombiaGamer's site
    """
    file_URIs = [f'file:{CGamer.TEST_PATH.value}/{file_name}' for file_name 
                in CGamer.TEST_FILES.value]
    
    process = CrawlerProcess()
    process.crawl(CGamerSpider, start_urls = file_URIs)
    process.start()


def _gamepl_setup():
    """
    Initializes the required conditions for testing on GamePlanet's site
    """
    fileURIs = [f'file:{GamePl.TEST_PATH.value}/{file_name}' for file_name 
                in GamePl.TEST_FILES.value]
    
    process = CrawlerProcess()
    process.crawl(GamePlSpider, start_urls = fileURIs)
    process.start()


def _mixup_setup():
    """
    Initializes the required conditions for testing on MixUp's site
    """
    fileURIs = [f'file:{MUC.TEST_PATH.value}/{file_name}' for file_name 
                in MUC.TEST_FILES.value]
    
    process = CrawlerProcess()
    process.crawl(MixUpSpider, start_urls = fileURIs)
    process.start()


def _sears_setup():
    """
    Initializes the required conditions for testing on Sears's site
    """
    fileURIs = [f'file:{SEA.TEST_PATH.value}/{file_name}' for file_name 
                in SEA.TEST_FILES.value]
    
    process = CrawlerProcess()
    process.crawl(SearSpider, start_urls = fileURIs)
    process.start()


def _assert_file_exists_and_matches_expected_value(file_path, expected):
    """
    This function tests the existence of the expected file and that it matches
    the expected data
    """
    file_message = f'expected the file {file_path} to exist'
    json_message = 'the exported json file does not match the expected result'
    
    assert os.path.exists(file_path), file_message

    with open(file_path) as json_file:
        data = json.load(json_file)
        assert data == expected, json_message


def _assert_files_exist_and_match_expected_value(file_paths, expected):
    """
    This function tests the existence of the expected files and that they 
    match the expected data
    """
    json_message = 'the exported json files don\'t match the expected result'

    data = []

    for path in file_paths:
        assert os.path.exists(path), f'expected the file {path} to exist'

        with open(path) as json_file:
            data.append(json.load(json_file)[0])
        
    assert data == expected, json_message


def test_olx_scrapper_happy_path_json_data_exported():
    """
    This test case checks if the scraper generates the right json file after
    scraping a mock with OLX's site structure
    """
    file_path = f'{OLX.EXPORT_FILE_PATH.value}'
    _cleanup(file_path)
    _olx_setup()

    _assert_file_exists_and_matches_expected_value(file_path,
                                                   OLX.TEST_PRODUCTS.value)
    _cleanup(file_path)


def test_cgamer_scrapper_happy_path_json_data_exported():
    """
    This test case checks if the scraper generates the right json file after
    scraping a mock with CGamer's site structure
    """
    file_path = f'{CGamer.EXPORT_FILE_PATH.value}'
    _cleanup(file_path)
    _cgamer_setup()

    _assert_file_exists_and_matches_expected_value(file_path,
                                                   CGamer.TEST_PRODUCTS.value)
    _cleanup(file_path)


def _map_responses(response_URIs, mock_URLs):
    """
    Maps mock responses to endpoints
    """
    for i in range(0, len(response_URIs)):
        with open(response_URIs[i], 'r', encoding = 'utf-8') as json_file:
            data = json.load(json_file)
            responses.add(responses.GET, mock_URLs[i],
                          json = data, status = 200)


@responses.activate
def test_mercadolibre_api_consuming_happy_path_json_data_exported():
    """
    This test case checks if MercadoLibre's API consuming generates the right
    json file after scraping a mock with MercadoLibre's expected responses
    """
    file_path = f'{MLC.EXPORT_FILE_PATH.value}'
    output_files = []

    for i in range(0, 3):
        index = f'{i}'.zfill(3)
        output_files.append(file_path.replace('.json', f'{index}.json'))
        _cleanup(output_files[i])

    _mercadolibre_setup()

    index_URIs = [f'{MLC.TEST_PATH.value}/{file_name}'
                  for file_name in MLC.TEST_INDEX_FILES_PARSED.value]
    
    _map_responses(index_URIs, MLC.TEST_INDEX_URLS.value)
    
    desc_URIs = [f'{MLC.TEST_PATH.value}/{file_name}'
                 for file_name in MLC.TEST_DESCRIPTION_FILES.value]

    _map_responses(desc_URIs, MLC.TEST_DESCRIPTION_URLS.value)

    detail_URIs = [f'{MLC.TEST_PATH.value}/{file_name}'
                   for file_name in MLC.TEST_PRODUCT_FILES_PARSED.value]

    _map_responses(detail_URIs, MLC.TEST_PRODUCT_URLS.value)

    apis.scrap_mercadolibre(0)

    _assert_files_exist_and_match_expected_value(output_files,
                                              MLC.TEST_PRODUCTS.value)

    index_mock_paths = [f'{MLC.TEST_PATH_RELATIVE.value}/{file_name}'
                        for file_name in MLC.TEST_INDEX_FILES_PARSED.value]
    product_mock_paths = [f'{MLC.TEST_PATH_RELATIVE.value}/{file_name}'
                          for file_name in MLC.TEST_INDEX_FILES_PARSED.value]
    
    for path in index_mock_paths:
        _cleanup(path)

    for path in product_mock_paths:
        _cleanup(path)

    for output_file in output_files:
        _cleanup(output_file)


def test_gamepl_scrapper_happy_path_json_data_exported():
    """
    This test case checks if the scraper generates the right json file after
    scraping a mock with GamePlanet's site structure
    """
    file_path = f'{GamePl.EXPORT_FILE_PATH.value}'
    _cleanup(file_path)
    _gamepl_setup()

    assert os.path.exists(file_path), f'expected the file {file_path} to exist'

    with open(file_path) as json_file:
        data = json.load(json_file)
        assert data == GamePl.TEST_PRODUCTS.value, \
                'the exported json file does not match the expected result'

    _cleanup(file_path)


def test_mixup_scrapper_happy_path_json_data_exported():
    """
    This test case checks if the scraper generates the right json file after
    scraping a mock with Mixup's site structure
    """
    file_path = f'{MUC.EXPORT_FILE_PATH.value}'
    _cleanup(file_path)
    _mixup_setup()

    assert os.path.exists(file_path), f'expected the file {file_path} to exist'

    with open(file_path) as json_file:
        data = json.load(json_file)
        assert data == MUC.TEST_PRODUCTS.value, \
                'the exported json file does not match the expected result'

    _cleanup(file_path)


def test_sears_scrapper_happy_path_json_data_exported():
    """
    This test case checks if the scraper generates the right json file after
    scraping a mock with Sears's site structure
    """
    file_path = f'{SEA.EXPORT_FILE_PATH.value}'
    _cleanup(file_path)
    _sears_setup()

    assert os.path.exists(file_path), f'expected the file {file_path} to exist'

    with open(file_path) as json_file:
        data = json.load(json_file)
        assert data == SEA.TEST_PRODUCTS.value, \
                'the exported json file does not match the expected result'

    _cleanup(file_path)

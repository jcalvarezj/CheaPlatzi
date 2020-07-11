"""
This module performs unit tests on the scraper module
"""
import os
import json
import pytest
import requests
import responses
from scrapy.crawler import CrawlerProcess
from ..utils import apis
from ..utils.spiders import OLXSpider, ColombiaGamerSpider as CGamerSpider
from ..utils.constants import MercadoLibreConfig as MLC
from ..utils.constants import OLXConfig as OLX, ColombiaGamerConfig as CGamer


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

            if not is_index:
                current_image = data['pictures'][0]['secure_url']
                new_value = ''

                if current_image == '$XBOXIMAGE':
                    new_value = f'file:{path}/xbox.jpg'
                elif current_image == '$SWITCHIMAGE':
                    new_value = f'file:{path}/switch.jpg'
                else:
                    new_value = f'file:{path}/play.jpg'                    

                data['pictures'][0]['secure_url'] = new_value
            else:
                current_link = data['results'][0]['permalink']
                new_value = ''

                if current_link == '$XBOXLINK':
                    new_value = f'file:{path}/xbox_mock.html'
                elif current_link == '$SWITCHLINK':
                    new_value = f'file:{path}/switch_mock.html'
                else:
                    new_value = f'file:{path}/playstation_mock.html'

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
    fileURI = f'file:{OLX.TEST_PATH.value}/{OLX.TEST_FILE.value}'

    process = CrawlerProcess()
    process.crawl(OLXSpider, start_urls = [fileURI])
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


def _assert_file_exists_and_matches_expected_value(file_path, expected):
    message = 'the exported json file does not match the expected result'

    assert os.path.exists(file_path), f'expected the file {file_path} to exist'

    with open(file_path) as json_file:
        data = json.load(json_file)
        
        assert data == expected, message


# def test_olx_scrapper_happy_path_json_data_exported():
#     """
#     This test case checks if the scraper generates the right json file after
#     scraping a mock with OLX's site structure
#     """
#     file_path = f'{OLX.EXPORT_FILE_PATH.value}'
#     _cleanup(file_path)
#     _olx_setup()

#     _assert_file_exists_and_matches_expected_value(file_path,
#                                                    OLX.TEST_PRODUCTS.value)
#     _cleanup(file_path)


# def test_cgamer_scrapper_happy_path_json_data_exported():
#     """
#     This test case checks if the scraper generates the right json file after
#     scraping a mock with CGamer's site structure
#     """
#     file_path = f'{CGamer.EXPORT_FILE_PATH.value}'
#     _cleanup(file_path)
#     _cgamer_setup()

#     _assert_file_exists_and_matches_expected_value(file_path,
#                                                    CGamer.TEST_PRODUCTS.value)
#     _cleanup(file_path)


def _add_responses(response_URIs, mock_URL):
    for i in range(0, len(response_URIs)):
        with open(response_URIs[i], 'r', encoding = 'utf-8') as json_file:
            print(f'Going to {response_URIs[i]}\n')
            data = json.load(json_file)
            print(f'Read {data}\n')
            print('ADDING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            responses.add(responses.GET, mock_URL,
                          json = data, status = 200)
            print(f'Addded {mock_URL} to mock {data}\n')


@responses.activate
def test_mercadolibre_api_consuming_happy_path_json_data_exported():
    """
    This test case checks if MercadoLibre's API consuming generates the right
    json file after scraping a mock with MercadoLibre's expected responses
    """
    _mercadolibre_setup()

    index_URIs = [f'{MLC.TEST_PATH.value}/{file_name}'
                  for file_name in MLC.TEST_INDEX_FILES_PARSED.value]
    
    _add_responses(index_URIs, MLC.SEARCH_URL.value)
    
    desc_URIs = [f'{MLC.TEST_PATH.value}/{file_name}'
                 for file_name in MLC.TEST_DESCRIPTION_FILES.value]

    _add_responses(desc_URIs, MLC.DESC_URL.value)

    detail_URIs = [f'{MLC.TEST_PATH.value}/{file_name.replace("base_", "")}'
                         for file_name in MLC.TEST_PRODUCT_FILES_PARSED.value]

    _add_responses(detail_URIs, MLC.DETAIL_URL.value)

    apis.scrap_mercadolibre(0)

    file_path = f'{CGamer.EXPORT_FILE_PATH.value}'
    output_file = file_path.replace('.json', '000.json')

    _assert_file_exists_and_matches_expected_value(output_file,
                                                   MLC.TEST_PRODUCTS.value)
    _cleanup(output_file)

    index_mock_paths = [f'{MLC.TEST_PATH_RELATIVE.value}/{file_name}'
                        for file_name in MLC.TEST_INDEX_FILES_PARSED.value]
    product_mock_paths = [f'{MLC.TEST_PATH_RELATIVE.value}/{file_name}'
                          for file_name in MLC.TEST_INDEX_FILES_PARSED.value]
    
    for path in index_mock_paths:
        _cleanup(path)

    for path in product_mock_paths:
        _cleanup(path)
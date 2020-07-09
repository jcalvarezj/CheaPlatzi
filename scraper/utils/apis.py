"""
This module contains the definiton of functions for API consuming
"""
import grequests
from .constants import HEADERS


def _handle_exception(request, exception):
    """
    Exception handler callback function
    """
    print('Could not perform the request due to a problem:')
    print(exception)


def _parse_endpoint(endpoint, params_dict):
    """
    Returns the endpoint with values parameters replaced with their values
    """
    parsed_endpoint = endpoint

    for param, value in params_dict.items():
        parsed_endpoint = parsed_endpoint.replace(param, value)

    return parsed_endpoint


def _print_response_success(response, index, expected_code, verbose):    
    request_url = response.request.url

    if response.status_code == expected_code:
        print(f'\n{"*" * 70}')
        print(f'SUCCESS! Obtained response #{index} for {request_url}\n')
        if verbose:
            print(response.json())
        print(f'{"*" * 70}\n')
    else:
        print(f'\n{"*" * 70}')
        print(f'Problem with the request to {request_url}. ')
        print(f'Response #{index}:')
        print(response.status_code)
        if verbose:
            print(response.json())
        print(f'{"*" * 70}\n')


def scrap_request(endpoints, params_dict = {}, verbose = False):
    """
    Attempts to send a GET request with for the specified list of endpoints for
    scraping
    
    The params_dict parameter is a dictionary of URL parameters to replace with
    values. The verbose flag enables showing the whole response contents (json)

    This method returns a list of response objects
    """
    pending_requests = []

    for endpoint in endpoints:
        parsed_endpoint = _parse_endpoint(endpoint, params_dict)

        pending_requests.append(grequests.get(parsed_endpoint,
                                              headers = HEADERS))

    responses = grequests.map(pending_requests,
                              exception_handler = _handle_exception)

    for i, response in enumerate(responses):
        if response != None:
            _print_response_success(response, i, 200, verbose)

    return responses


def store_request(page_list, endpoint, verbose):
    """
    Attempts to send multiple asynchronous POST requests to the specified
    endpoint, one for each element of the page list
    """
    pending_requests = []

    for page_data in page_list:
        print(f'The data to send is\n{page_data}')
        pending_requests.append(grequests.post(endpoint, data = page_data,
                                               headers = HEADERS))    
    responses = grequests.map(pending_requests, 
                              exception_handler = _handle_exception)
    
    for i, response in enumerate(responses):        
        if response != None:
            _print_response_success(response, i, 201, verbose)
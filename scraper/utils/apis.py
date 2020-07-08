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


def send_request(endpoints, params_dict = {}, verbose = False, delay = None):
    """
    Attempts to send a request with for the specified list of endpoints.
    If the endpoints have $SITE_ID and $CATEGORY_ID URL parameters, the 
    country_id and category_id parameters are respectively required

    This method returns a list of response objects
    """
    pending_requests = []

    for endpoint in endpoints:
        parsed_endpoint = _parse_endpoint(endpoint, params_dict)

        pending_requests.append(grequests.get(parsed_endpoint,
                                              headers = HEADERS))

    responses = grequests.map(pending_requests,
                              exception_handler = _handle_exception)

    for index, response in enumerate(responses):
        if response:
            request_url = response.request.url

            if response.status_code == 200:
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

    return responses
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


def send_request(endpoints, country_id = "", category_id = "",
                 verbose = False):
    """
    Attempts to send a request with for the specified list of endpoints.
    If the endpoints have $SITE_ID and $CATEGORY_ID URL parameters, the 
    country_id and category_id parameters are respectively required

    This method returns a list of response objects
    """
    pending_requests = []

    for endpoint in endpoints:
        parsed_endpoint = endpoint.replace('$SITE_ID', country_id) \
                              .replace('$CATEGORY_ID', category_id)

        pending_requests.append(grequests.get(parsed_endpoint,
                                              headers = HEADERS))

    responses = grequests.map(pending_requests,
                              exception_handler = _handle_exception)

    for index, response in enumerate(responses):
        r_url = response.request.url

        if response.status_code == 200:
            print(f'\n{"*" * 70}')
            print(f'SUCCESS! Obtained response #{index} for {r_url}\n')
            if verbose:
                print(response.json())
            print(f'{"*" * 70}\n')
        else:
            print(f'\n{"*" * 70}')
            print(f'Problem with the request to {r_url}. ')
            print(f'Response #{index}:')
            print(response.status_code)
            if verbose:
                print(response.json())
            print(f'{"*" * 70}\n')

    return responses
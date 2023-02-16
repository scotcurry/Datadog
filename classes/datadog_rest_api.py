import os
import logging
import sys

import requests

rest_api_key = os.getenv('DD_API_KEY')
rest_application_key = os.getenv('DD_APPLICATION_KEY')


logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

base_api_url = 'https://api.datadoghq.com/api'
headers = {'Content-Type': 'application/json', 'DD_API_KEY': rest_api_key, 'DD_APPLICATION_KEY':
        rest_application_key}


def validate_api_keys():

    print('REST API Key: ' + rest_api_key)
    print('REST Application Key: ' + rest_application_key)
    return_value = False
    endpoint = '/v1/validate'
    uri = base_api_url + endpoint
    api_test = requests.get(uri, headers=headers)

    rest_body = api_test.json()
    for keys in rest_body:
        return_value = rest_body[keys]

    return return_value


def get_usage_by_product_family():


    endpoint = '/v1/usage/summary'
    parameters = {'start_month': '2022-12'}
    uri = base_api_url + endpoint
    product_usage = requests.get(url=uri, headers=headers, params=parameters)

    value = 0
    rest_body = product_usage.json()
    for key in rest_body:
        if key == 'aws_lambda_func_count':
            value = rest_body[key]

    return value
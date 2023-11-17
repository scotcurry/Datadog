from classes.datadog_rest_api import get_usage_by_product_family
from classes.flaky_test import flaky_test

def test_validate_tests_work():
    variable = 'Otis'
    assert 'O' in variable

def test_datadog_usage_summary():
    api_return = get_usage_by_product_family()
    assert api_return > 0

def test_flak_test():
    value = flaky_test()
    assert value > 3
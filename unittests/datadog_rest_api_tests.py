from classes.datadog_rest_api import validate_api_keys, get_usage_by_product_family
def test_validate_tests_work():
    variable = 'Otis'
    assert 'O' in variable

def test_validate_api_key():
    api_return = validate_api_keys()
    assert api_return is True

def test_datadog_usage_summary():
    api_return = get_usage_by_product_family()
    assert api_return > 0
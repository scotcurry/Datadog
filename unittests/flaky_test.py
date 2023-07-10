from classes.flaky_test import flaky_test


def test_flak_test():
    value = flaky_test()
    assert value > 5

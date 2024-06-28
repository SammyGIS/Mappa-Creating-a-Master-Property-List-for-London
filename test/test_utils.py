import pytest
from selenium import webdriver

from utils.utils import get_driver

from utils.utils import get_driver


@pytest.fixture(scope="module")
def driver():
    # Test driver for get_pages function
    return get_driver()

def test_get_driver(driver):
    # test driver locatoion
    assert isinstance(driver, webdriver.Chrome)


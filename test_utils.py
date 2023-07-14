import pytest
from utils  import get_driver, merge_save
import pandas as pd
from selenium import webdriver

@pytest.fixture(scope="module")
def driver():
    # Test driver for get_pages function
    return get_driver()

def test_get_driver(driver):
    # test driver locatoion
    assert isinstance(driver, webdriver.Chrome)
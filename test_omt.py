import pytest
from _omt_scraper import get_driver, get_pages, extract_data, get_data
import pandas as pd
from selenium import webdriver

@pytest.fixture(scope="module")
def driver():
    # Test driver for get_pages function
    return get_driver()

@pytest.fixture(scope="module")
def page_html(driver):
    # Test page_html for extract_data function
    url = 'https://www.onthemarket.com/to-rent/property/london/?page={}&view=grid'
    page = 1
    return get_pages(driver, page, url)

def test_get_driver():
    driver = get_driver()
    assert isinstance(driver, webdriver.Chrome)

def test_get_pages(driver):
    url = 'https://www.onthemarket.com/to-rent/property/london/?page={}&view=grid'
    page = 1
    page_html = get_pages(driver, page, url)
    assert isinstance(page_html, list)
    assert len(page_html) > 0

def test_extract_data(page_html):
    transaction_type = 'rent'
    source = 'omt'
    data = extract_data(page_html, transaction_type, source)
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_data():
    url = 'https://www.onthemarket.com/to-rent/property/london/?page={}&view=grid'
    transaction_type = 'rent'
    source = 'omt'
    start_page = 1
    end_page = 2
    data = get_data(url, transaction_type, source, start_page, end_page)
    assert isinstance(data, pd.DataFrame)
    assert len(data) > 0



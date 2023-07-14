import pytest
from _zoopla_scaper import get_driver, get_pages, extract_data, get_data
import pandas as pd
from selenium import webdriver
import undetected_chromedriver as uc
WEB_URL ='https://www.zoopla.co.uk/to-rent/property/london/?\
    price_frequency=per_month&q=london&results_sort=newest_listings&search_source=to-rent&pn={}_next'

@pytest.fixture(scope="module")
def driver():
    # Test driver for get_pages function
    return get_driver()

@pytest.fixture(scope="module")
def page_html(driver):
    # Test page_html for extract_data function
    url = WEB_URL
    page = 1
    return get_pages(driver, page, url)

def test_get_driver(driver):
    assert isinstance(driver, webdriver.Chrome)

def test_get_pages(page_html):
    assert isinstance(page_html, list)
    assert len(page_html) > 0

def test_extract_data(page_html):
    transaction_type = 'rent'
    source = 'omt'
    data = extract_data(page_html, transaction_type, source)
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_data():
    url = WEB_URL
    transaction_type = 'rent'
    source = 'zoopla'
    start_page = 1
    end_page = 2
    data = get_data(url, transaction_type, source, start_page, end_page)
    assert isinstance(data, pd.DataFrame)
    assert len(data) > 0
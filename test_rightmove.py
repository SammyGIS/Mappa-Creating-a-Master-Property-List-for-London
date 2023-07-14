import pytest
import pandas as pd
from utils import get_driver
from _rightnow_scaper import  get_pages, extract_data, get_data

WEB_URL = "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E87490&index={}\
        &propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="

# create a fixture module that only runs one when u run the code and can be reusable by other functions 
@pytest.fixture(scope='module')
def driver():
    # calll on the driver function from utils as a module
    return get_driver()

# create a fixture module that only runs one when u run the code and can be reusable by other functions 
@pytest.fixture(scope='module')
def page_html(driver):
    # call a function and test it with the follwoing arameters
    url = WEB_URL
    page = 1
    get_html = get_pages(driver,page,url)
    return get_html

def test_get_pages(page_html):
    # test if the get page instance that was callled as a model above returns a list of html pages
    assert isinstance(page_html, list)
    #check the list if is empty or not
    assert len(page_html) > 0

def test_extract_data(page_html):
    transaction_type = 'rent'
    source = 'rightmove'
    extractdata = extract_data(page_html,transaction_type,source)
    # test if the get page instance that was callled as a model above returns a list of html pages
    assert isinstance(extractdata,list)
    #check the list if is empty or not
    assert len(extractdata) > 0

def test_get_data():
    url = WEB_URL
    transaction_type = 'rent'
    source = 'rightmove'
    start_index = 1
    stop_index = 2
    increment = 1
    data = get_data(url, transaction_type, source, start_index, stop_index, increment)
    assert isinstance(data, pd.DataFrame)
    assert len(data) > 0
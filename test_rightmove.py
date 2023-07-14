import pytest
import pandas as pd
from utils import get_driver
from _rightnow_scaper import  get_pages, get_data, extract_data

# create a fixture module that only runs one when u run the code and can be reusable by other functions 
@pytest.fixture(scope='module')
def driver():
    # calll on the driver function from utils as a module
    return get_driver()

# create a fixture module that only runs one when u run the code and can be reusable by other functions 
@pytest.fixture(scope='module')
def page_html(driver):
    # call a function and test it with the follwoing arameters
    url = "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E87490&index={}\
        &propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="
    page = 1
    get_html = get_pages(driver,page,url)
    return get_html


def test_get_pages(page_html):
    # test if the get page instance that was callled as a model above returns a list of html pages
    assert isinstance(page_html, list)
    #check the list if is empty or not
    assert len(page_html) > 0

def test_get_pages():
#     pass

# def test_extract_data():
#     pass
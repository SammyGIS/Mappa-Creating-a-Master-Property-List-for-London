from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import pandas as pd

def get_driver():

    try:
        options = webdriver.ChromeOptions()
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptInsecureCerts'] = True

        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(r'C:\Windows\chromedriver.exe', options=options, desired_capabilities=capabilities)
        
        return driver
    
    except Exception as e:
        print(e)

def merge_save(rents_data,sales_data):
    """
    Takes two DataFrame, merged the data and then save the daa to a folder as csv file

    Args:
        - rent_data (DataFrame): The dataframe of the rent daset
        - sales_data (DataFrame): The type of transaction for which information needs to be extracted.

    Returns:
        dataframe containing the data sccrapped from the website   
    """
    # merged the two data
    appended_data = pd.concat([rents_data, sales_data])

    #save it as csv
    path = 'data_output'
    if not os.path.exists(path):
        os.mkdir(path)
    
    # save the combined data to csv within the path
    appended_data.to_csv(f'{path}/omt_{date.today()}.csv', index=False)
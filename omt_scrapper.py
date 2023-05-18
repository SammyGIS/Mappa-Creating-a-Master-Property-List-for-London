
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
import datetime
from datetime import datetime, date
import time


om_renturl  = 'https://www.onthemarket.com/to-rent/property/london/?page={}&view=grid'
om_salesurl  = 'https://www.onthemarket.com/for-sale/property/london/?page={}&view=grid'


def get_driver():
    options = webdriver.ChromeOptions()

    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptInsecureCerts'] = True

    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(r'C:\Windows\chromedriver.exe', options=options, desired_capabilities=capabilities)
    
    return driver

def get_pages(driver,page,url):
    driver.get(url.format(page))
    OM_DIV_TAG = 'otm-PropertyCard '
    page_html = driver.find_elements(By.CLASS_NAME, OM_DIV_TAG)
    return page_html

def parse_pages(page_html:'page_html', transaction_type:str, source:str):
    """
    
    """
    page_data = []

    for page in page_html:
        # Transaction

        try:
            if transaction_type == 'rent':
                transaction = transaction_type

            elif transaction_type == 'sales':
                transaction = transaction_type

            else:
                print('transaction_type can either be sales or rent')
                break

        except:
                print('transaction_type can either be sales or rent')
                break
        

        # time.sleep(3)
        # Address
        try:
            address_tag = page.find_element(By.CLASS_NAME, 'address')
            address = address_tag.text 

        except:
            address = ''


        # time.sleep(3)
        # Bedroom
        try:         
            
            bedroom_element = page.find_element(By.CLASS_NAME,"otm-BedBathCount")
            bedroom = bedroom_element.text.split("\n")[0].strip()

        except:
            bedroom = ''

        # time.sleep(3)
        # Bathroom
        try:
            
            bathroom_tag = page.find_element(By.CLASS_NAME,"otm-BedBathCount")
            bathroom = bathroom_tag.text.split("\n")[1].strip()

        except:
            bathroom =''

        # time.sleep(3)
        # Description
        try:
            description_tag = page.find_element(By.CLASS_NAME, ' ')
            description = description_tag.text

        except:
            description = ''


        # property Type
        try:
            property_type_tag =page.find_element(By.CLASS_NAME, 'title')
            property_type = property_type_tag.text.split("\n")[0].strip()

        except:
            property_type = ''


            # price
    
        # time.sleep(3)
        # rent payment
        if transaction_type == 'rent':

            sales_price = ' '
            
            # rent price per month
            try:
                price_tag= page.find_element(By.CLASS_NAME, 'otm-Price')
                price = price_tag.text.split("\n")[-1].strip()
                per_month = price.split("pcm")[0].strip().split("£")[1].split(" ")[0]
                
            except:
                per_month = ''
                
            # rent price per week
            try:
                price_tag= page.find_element(By.CLASS_NAME, 'otm-Price')
                price = price_tag.text.split("\n")[-1].strip()
                per_week = price.split("pcm")[-1].strip().split("£")[1].split(" ")[0]

            except:
                per_week = ''               

        else:
            # sales Price
            try:
                per_week = ''  
                per_month = ''
                
                price_tag = page.find_element(By.CLASS_NAME, 'otm-Price')
                sales_price = price_tag.text.split("\n")[-1].strip()
                
            except:
                sales_price = ' '

        # time.sleep(3)           
        # Location
        try:
            location_tag = page.find_element(By.CLASS_NAME, 'address')
            location = location_tag.text.split(" ")[-1].strip()
        
        except:
            location =''
    
        # time.sleep(3)
        # Agent
        try: 
            agent_tag = page.find_element(By.CLASS_NAME, 'agent-logo')
            agent_tag = agent_tag.find_element(By.TAG_NAME, 'img')            
            agent = agent_tag.get_attribute('alt')
            
        except:
            agent = ''


        #Listing Source
        listing_source = source

        # time.sleep(3)
        # Listing URL

        try:
            
            listing_url_tag =page.find_element(By.CLASS_NAME, 'agent-logo')
            listing_url_tag =listing_url_tag.find_element(By.TAG_NAME, 'a')
            listing_url = listing_url_tag.get_attribute('href')

        except:
            listing_url = ''
        
        # time.sleep(3)
        # Date Added
        try:
            date_added_tag = page.find_element(By.CLASS_NAME, 'days-otm')
            date_added = date_added_tag.text.split("OnTheMarket")[-1].strip()
            
        except:
            date_added = ' '
            
            
        page_data.append({
            'transaction': transaction,
            'address': address,
            'bedroom': bedroom,
            'bathroom': bathroom,
            'sales_price': sales_price,
            'rent_perMonth': per_month,
            'rent_perWeek': per_week,
            'description': description,
            'propertyType': property_type,
            'location':location,
            'agent':agent,
            'listing_source':listing_source,
            'listing_url':listing_url,
            'date_added ': date_added ,
            })

    return page_data


def get_data(url,transaction_type,source,start_page, end_page):
    browser = get_driver()
    all_pages_data = []
    
    for page in range(start_page, end_page+1):
        time.sleep(1)
        page_html = get_pages(browser,page,url)
        time.sleep(1)
        pages_data = parse_pages(page_html,transaction_type, source)
        time.sleep(1)
        all_pages_data.extend(pages_data)
        time.sleep(1)

    browser.quit()

    data = pd.DataFrame(all_pages_data)
    return data

if __name__ == "__main__":
    # Specify the start and end page numbers for scraping
    start_page = 1
    end_page = 42

    # Call the get_data function to scrape the data
    rent_data = get_data(om_renturl,'rent','omt',start_page, end_page)
    sales_data = get_data(om_salesurl,'sales','pmt',start_page, end_page)


    # merged the two data
    appended_data = pd.concat([rent_data, sales_data])

    #save it as csv
    appended_data.to_csv(f'omt_{date.today()}.csv', index=False)

    # save scrapped data to csv

    print('data scraped successfully')    
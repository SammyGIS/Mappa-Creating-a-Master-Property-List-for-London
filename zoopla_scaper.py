from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import datetime
from datetime import datetime



zrent_url = 'https://www.zoopla.co.uk/to-rent/property/london/?price_frequency=per_month&q=london&results_sort=newest_listings&search_source=to-rent&pn={}'
zsales_url = 'https://www.zoopla.co.uk/for-sale/property/london/?price_frequency=per_month&q=london&results_sort=newest_listings&search_source=to-rent&pn={}'

def get_driver():
    # path to chrome driver on my pc
    driver = webdriver.Chrome(r'C:\Windows\chromedriver.exe')
    return driver

def get_pages(driver,page,url):
    driver.get(url.format(page))
    OM_DIV_TAG = 'kii3au6'
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
        
        # Address
        try:
            address_tag = page.find_element(By.CLASS_NAME, "_1ankud52")
            address = address_tag.text
        except:
            address = ''

        # Bedroom
        try:         
            
            bedroom_element = page.find_element(By.CLASS_NAME,"_1ljm00u3z    ")
            if bedroom_element.text.split("\n")[0].strip() == 'Bedrooms':
                bedroom = bedroom_element.text.split("\n")[1].strip()
            else:
                bedroom = ''

        except:
            bedroom = ''
     
        # Bathroom
        try:
            
            bathroom_tag = page.find_element(By.CLASS_NAME,"_1ljm00u3z    ")
            if bathroom_tag.text.split("\n")[0].strip() == 'Bathrooms':
                bathroom = bathroom_tag.text.split("\n")[1].strip()

            elif bathroom_tag.text.split("\n")[2].strip() == 'Bathrooms':
                bathroom = bathroom_tag.text.split("\n")[3].strip()

            else:
                bathroom = ''
        except:
            bathroom =''


        # Living room

        try:
            
            livingroom_tag = page.find_element(By.CLASS_NAME,"_1ljm00u3z    ")
            if livingroom_tag.text.split("\n")[0].strip() == 'Living rooms':
                living_room = livingroom_tag.text.split("\n")[1].strip()

            elif livingroom_tag.text.split("\n")[2].strip() == 'Living rooms':
                living_room = livingroom_tag.text.split("\n")[3].strip()

            elif livingroom_tag.text.split("\n")[4].strip() == 'Living rooms':
                living_room = livingroom_tag.text.split("\n")[5].strip()

            else:
                living_room = ''
        except:
            living_room =''


        # Description
        try:
            description_tag = page.find_element(By.CLASS_NAME, '_1ankud53')
            description = description_tag.text

        except:
            description = ''


        # property Type
        try:
            property_type_tag =page.find_element(By.CLASS_NAME, '_1ankud51')
            property_type = property_type_tag.text.split("\n")[0].strip()

        except:
            property_type = ''

  
        # rent payment
        if transaction_type == 'rent':

            sales_price = ' '
            
            # rent price per month
            try:
                pcm = page.find_element(By.CLASS_NAME, '_170k6632')
                per_month = pcm.text.split(" ")[0].strip()
                
            except:
                per_month = ''
                
            # rent price per week
            try:
                pw = page.find_element(By.CLASS_NAME, '_170k6633')
                per_week = pw.text.split(" ")[0].strip()

            except:
                per_week = ''               

        else:
            # sales Price
            try:
                per_week = ''  
                per_month = ''
                
                price_tag = page.find_element(By.CLASS_NAME, '_170k6632 ')
                sales_price = price_tag.text.split(" ")[0].strip()
                
            except:
                sales_price = ' '
           
        # Location
        try:
            location_tag = page.find_element(By.CLASS_NAME, '_1ankud52')
            location = location_tag.text.split(",")[-1].strip()
        
        except:
            location =''
    

        # Agent
        try: 
            agent_tag =page.find_element(By.CLASS_NAME, '_12bxhf70')
            # print(agent_tag.get_attribute('innerHTML'))
            agent = agent_tag.get_attribute('alt')
            
        except:
            agent = ''


        #Listing Source
        listing_source = source

        # Listing URL
        try:
            listing_url_tag =page.find_element(By.CLASS_NAME, '_1maljyt1')
            listing_url = listing_url_tag.get_attribute('href')

        except:
            listing_url = ''
        

        # Date Added
        try:
            date_tag = page.find_element(By.CLASS_NAME, '_18cib8e1')
            date_string = date_tag.text.split(" on ")[-1].strip()
            listed_date = datetime.strptime(date_string,"%dth %B %Y").strftime("%d-%m-%Y")
            
        except:
            listed_date = ' '
            
            
        page_data.append({
            'transaction': transaction,
            'address': address,
            'bedroom': bedroom,
            'bathroom': bathroom,
            'living_room': living_room,
            'sales_price': sales_price,
            'rent_perMonth': per_month,
            'rent_perWeek': per_week,
            'description': description,
            'propertyType': property_type,
            'location':location,
            'agent':agent,
            'listing_source':listing_source,
            'listing_url':listing_url,
            'listed_date': listed_date,
            })

    return page_data


def get_data(url,transaction_type,source,start_page, end_page):
    browser = get_driver()
    all_pages_data = []

    for page in range(start_page, end_page+1):
        page_html = get_pages(browser,page,url)
        pages_data = parse_pages(page_html,transaction_type, source)
        all_pages_data.extend(pages_data)

    browser.quit()

    data = pd.DataFrame(all_pages_data)
    return data


if __name__ == "__main__":
    # Specify the start and end page numbers for scraping
    start_page = 1
    end_page = 1

    # Call the get_data function to scrape the data
    rent_data = get_data(zrent_url,'rent','zoopla',start_page, end_page)
    sales_data = get_data(zsales_url,'sales','zoopla',start_page, end_page)

    # merged the two data
    appended_data = pd.concat([rent_data, sales_data])

    #save it as csv
    appended_data.to_csv(f'zoopla_{datetime.date.today()}.csv', index=False)

    # save scrapped data to csv

    print('data scrapped successfully')    
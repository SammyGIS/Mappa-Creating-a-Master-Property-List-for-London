from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import datetime



rm_salesurl = "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E87490&index={}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="
rm_renturl = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87490&index={}&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords="


def get_driver():
    # path to chrome driver on my pc
    driver = webdriver.Chrome(r'C:\Windows\chromedriver.exe')
    return driver


def get_pages(driver,page,url):
    driver.get(url.format(page))
    OM_DIV_TAG = 'propertyCard-wrapper'
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
            address_tag = page.find_element(By.CLASS_NAME, "propertyCard-address")
            address = address_tag.text
        except:
            address = ''

        # Bedroom
        try:         
            bedroom_element = page.find_element(By.CLASS_NAME,"propertyCard-content")
            bedroom_span = bedroom_element.find_element(By.CLASS_NAME, "bed-icon")
            inner_html = bedroom_span.get_attribute('innerHTML')

            # use string formatting
            title_start = "<title>"
            title_end = "</title>"
            title_index_start = inner_html.index(title_start) + len(title_start)
            title_index_end = inner_html.index(title_end)
            bedroom = inner_html[title_index_start:title_index_end][0:1]    

            #.text.split("\n")[-1].strip()
            # bedroom = bedroom_span.get_attribute('innerHTML')
            # print(bedroom)
            # # print(bedroom_span.get_attribute('title')        
        
        except:
            bedroom = ''
     
       
        
        # Bathroom
        try:
            
            bathroom_tag =page.find_element(By.CLASS_NAME,"propertyCard-content")
            bathroom_span = bathroom_tag.find_element(By.CLASS_NAME, "bathroom-icon")
            inner_html2 = bathroom_span.get_attribute('innerHTML')

            # use string formatting
            title_start = "<title>"
            title_end = "</title>"
            title_index_start = inner_html2.index(title_start) + len(title_start)
            title_index_end = inner_html2.index(title_end)
            bathroom = inner_html2[title_index_start:title_index_end][0:1]    

        except:
            bathroom =''


        # Description
        try:
            description_tag = page.find_element(By.CLASS_NAME, 'propertyCard-description')
            description = description_tag.text

        except:
            description = ''


        # property Type
        try:
            property_type_tag =page.find_element(By.CLASS_NAME, 'property-information')
            property_type =property_type_tag.text.split("\n")[0].strip()

        except:
            property_type = ''

  
        # rent payment
        if transaction_type == 'rent':

            sales_price = ' '
            
            # rent price per month
            try:
                pcm = page.find_element(By.CLASS_NAME, 'propertyCard-priceValue')
                per_month = pcm.text.split(" ")[0].strip()
                
            except:
                per_month = ''
                
            # rent price per week
            try:
                pw = page.find_element(By.CLASS_NAME, 'propertyCard-secondaryPriceValue')
                per_week = pw.text.split(" ")[0].strip()

            except:
                per_week = ''               

        else:
            # sales Price
            try:
                per_week = ''  
                per_month = ''
                
                price_tag = page.find_element(By.CLASS_NAME, 'propertyCard-priceValue')
                sales_price = price_tag.text.split(" ")[0].strip()
                
            except:
                sales_price = ' '

                

        # Location
        try:
            location_tag = page.find_element(By.CLASS_NAME, 'propertyCard-address')
            location = location_tag.text.split(",")[-1].strip()
        
        except:
            location =''
    

        # Agent
        try: 
            agent_tag =page.find_element(By.CLASS_NAME, 'propertyCard-branchSummary')
            # print(agent_tag.get_attribute('innerHTML'))
            agent = agent_tag.text.split("by")[-1].strip()

        except:
            agent = ''

        #Listing Source
        listing_source = source

        # Listing URL
        try:
            listing_url_tag =page.find_element(By.CLASS_NAME, 'propertyCard-link')
            listing_url = listing_url_tag.get_attribute('href')

        except:
            listing_url = ''
        

        
        # Date Added
        try:
            date_tag = page.find_element(By.CLASS_NAME, 'propertyCard-branchSummary-addedOrReduced')
            # print(date_tag.get_attribute('innerHTML'))
            added_reduced = date_tag.text
            date_type = date_tag.text.split(" ")[0].strip()

            # date
            if added_reduced == 'Added today':
                date = datetime.date.today()
                
            elif added_reduced== 'Added yesterday':
                date = datetime.date.today() - timedelta(days=1)

            elif added_reduced== 'Reduced today':
                date = datetime.date.today()

            elif added_reduced== 'Reduced yesterday':
                date = datetime.date.today() - timedelta(days=1)

            else:
                date = date_tag.text.split()[-1].strip()
        except:
            date = ' '
            date_type = ' '      


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
            'date_type':date_type,
            'date':date,
            })

    return page_data


def get_data(url,transaction_type,source,start_index, stop_index,increment):
    browser = get_driver()
    all_pages_data = []

    for page in range(start_index, stop_index,increment):
        page_html = get_pages(browser,page,url)
        pages_data = parse_pages(page_html,transaction_type, source)
        all_pages_data.extend(pages_data)

    browser.quit()

    data = pd.DataFrame(all_pages_data)
    return data

if __name__ == "__main__":
    # Specify the start and end page numbers for scraping
    start_index = 0
    stop_index = 1100
    increment = 24    

    # Call the get_data function to scrape the data
    rent_data = get_data(rm_renturl,'rent','rightmove',start_index, stop_index,increment)
    sales_data = get_data(rm_salesurl,'sales','rightmove',start_index, stop_index,increment)


    # merged the two data
    appended_data = pd.concat([rent_data, sales_data])

    #save it as csv
    appended_data.to_csv(f'rightnow_{datetime.date.today()}.csv', index=False)

    # save scrapped data to csv

    print('data scapped successfully')    
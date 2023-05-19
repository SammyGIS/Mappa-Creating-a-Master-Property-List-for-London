## Project Brief

From finding a new neighbourhood, to property viewings, negotiations and dealing with admin (e.g. mortgage and legal), your decision-making potential will be maximised to allow you secure the best value for your money.

Our mission is to hand back knowledge and control to the house hunter using the power of data and technology.

Our goal with this project is to create a master list of listed properties starting with London. Your task is the extract and blend property datasets across the Greater London area (United Kingdom) in one dataset.

## Key Deliverables:
Code base
Documentation
Architecture diagram of flow

## Dataset from Property sites
Rightmove
Zoopla
On The Market (OTM)

## Required fields
* Transaction type (i.e. sale vs. rent - string)
* Bedrooms (integer)
* Bathrooms (integer)
* Description (free text string)
* Property type e.g. flat, detached house, terraced house
* Price e.g. 500,000 (typically integer)
* Location :  Key location data here is Postcode district and/or Postcode
* Agent (advertising the property)
* Listing source
* Listing URL
* Other nice-to-have metadata
* If a rental property is furnished or not
* Anything else you deem interesting

## Geographical remit
Greater London: List of postcode districts

## Prerequisites
* [Seeting up Seleium](https://www.geeksforgeeks.org/how-to-install-selenium-in-python/)
* Python 3.x
* Selenium library
* undetected_chromedriver library
* psycopg2 library
* pandas library
* Chrome WebDriver (chromedriver.exe) placed in the specified location

## Usage
1. Clone the repository or download the script.

```
git clone https://github.com/SammyGIS/Flood-Modeeling-using-ML.git
```

2. Install the required libraries by running the following command:
```
pip install  package
```

3. Make sure you have the Chrome WebDriver (chromedriver.exe) placed in the specified location.

4. Update the start and end page numbers in the `if __name__ == "__main__":` section according to your requirements.

5. Run the script:

6. The scraped data will be saved as a CSV file in the current directory with the name `zoopla_<current_date>.csv`.


## Call the get_data function to scrape the data
```
rent_data = get_data(zrent_url, 'rent', 'zoopla', start_page, end_page)

```
```
sales_data = get_data(zsales_url, 'sales', 'zoopla', start_page, end_page)
```


Feel free to customize the script and modify it according to your needs.

If you encounter any issues or have suggestions for improvements, please feel free to submit an issue or a pull request.

Happy scraping!
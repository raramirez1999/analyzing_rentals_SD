import pandas as pd
import requests
import warnings
import creds

# Suppress warnings and set display options for pandas DataFrame
warnings.filterwarnings("ignore")
pd.set_option("display.max_columns", None)

def get_listings(api_key, listing_url):
    # Function to make API request from "Scrapeak" API to get rental listings data from Zillow
    url = "https://app.scrapeak.com/v1/scrapers/zillow/listing"

    # Define the parameters for the API request
    querystring = {
        "api_key": api_key,
        "url": listing_url
    }

    # Send the API request and get the response
    response = requests.request("GET", url, params=querystring)

    # Check if the API request was successful (status code 200) and extract data (if available)
    if response.status_code == 200:
        data = response.json()
        if "cat1" in data.get("data", {}):
            return data["data"]["cat1"]["searchResults"]["mapResults"]
    return []

# Refer to the API key from the creds.py file
api_key = creds.api_key

# Zillow search URL. Replace URL here for a new Zillow search
rent_listing_url = "https://www.zillow.com/san-diego-county-ca/rentals/?searchQueryState=%7B%22mapBounds%22%3A%7B%22north%22%3A32.972391013354944%2C%22east%22%3A-116.78582647840257%2C%22south%22%3A32.712788836483014%2C%22west%22%3A-117.23145941297288%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22beds%22%3A%7B%22min%22%3A4%2C%22max%22%3A4%7D%2C%22baths%22%3A%7B%22min%22%3A2%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A2841%2C%22regionType%22%3A4%7D%5D%2C%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Diego%20County%20CA%22%2C%22mapZoom%22%3A12%7D"

# Get rental listings data from Zillow using the provided URL
rent_listings_data = get_listings(api_key, rent_listing_url)

# Convert the data to a DataFrame if it is not empty
if rent_listings_data:
    df_rent_listings = pd.json_normalize(rent_listings_data)

    # Display basic information about the DataFrame
    print("Number of rows:", len(df_rent_listings))
    print("Number of columns:", len(df_rent_listings.columns))
    print(df_rent_listings.head())

    # Save the rental listings DataFrame to a CSV file
    df_rent_listings.to_csv('renting_listings_vs.csv')
else:
    print("No rental listings data available.")
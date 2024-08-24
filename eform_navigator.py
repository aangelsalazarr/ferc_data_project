import requests 

# selenium related tools
from selenium import webdriver


# this is node naught, where we begin our navigation journey
eform_url = "https://ecollection.ferc.gov/submissionHistory"

# setting up the driver path 
driver_path = ''

# we are selecting chrome as our driver manager?
driver = webdriver.Chrome()

# opening the ferc eform page
driver.get(url=eform_url)

# allowing the website to load for 3 seconds
driver.implicitly_wait(time_to_wait=3)

'''
objects and areas that we can filter for on the webpage

1. CID: String Input
2. Company: Strig Input
3. Form: String or Checkbox Input
4. Year: String Input (YYYY)
5. Period: String or Checkbox Input (Q1)
6. Date/Time: Start/End Input (mm/dd/yyyy)
7. Status: String or Checkbox Input (Accepted or Migrated)
8. Filing ID:


'''
import requests 
import time

# selenium related tools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# this is node naught, where we begin our navigation journey
eform_url = "https://ecollection.ferc.gov/submissionHistory"

# setting up the driver path 
driver_path = ''

# we are selecting chrome as our driver manager?
driver = webdriver.Chrome()

# opening the ferc eform page
driver.get(url=eform_url)

# waiting for the webpage to fully load
# wait for options to be available
wait = WebDriverWait(driver, 10)
options = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//mat-option")))


'''# allowing the website to load for 7 seconds
driver.implicitly_wait(time_to_wait=7)

# letting the webpage chill out for a bit to allow for the eforms site to load
# webpage loads in a little under 10 seconds so setting at 10 should be sufficient
time.sleep(10)'''

# setting up the clicking of the Year column carrot via xpath
year_col_button_path = '//*[@id="caret-down"]'

# this is where we input the year string YYYY
year_input_str = '/html/body/div/app-root/submission-history/div/ag-grid-angular/div/div[3]/div/div/div/div[1]/div[1]/div[1]'

# this code clicks on the carrot drop down for year col specifically
year_col_filter = driver.find_element(By.XPATH, year_col_button_path)
year_col_filter.click()


# closing the window of our loaded webpage
driver.quit()
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

# xpath locating the upper left cell within the eform table
eform_tbl_row1 = '/html/body/div/app-root/submission-history/div/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div/div[1]/div[1]'

# waiting for webpage to fully load and we know this by the existence of the table with form data
WebDriverWait(driver, 17).until(EC.presence_of_all_elements_located((By.XPATH, eform_tbl_row1)))

# letting the user know that the eform table has been identified
print('Table containing eforms is present (=')

# now we want to filter out by year
year_button_path = '/html/body/div/app-root/submission-history/div/ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div/div[4]/div[3]/span'
year_button = driver.find_element(By.XPATH, year_button_path)
year_button.click()

# now we want to input string value represetning year we would like to filter for year, e.g. 2024
year_filter_input = '/html/body/div/app-root/submission-history/div/ag-grid-angular/div/div[3]/div/div/div/div[1]/div[1]/div[1]/input'
year_filter = driver.find_element(By.XPATH, year_filter_input)
year_filter.send_keys('2024')

# purpose is to click apply filter on the year filter
apply_year_filter_path = '/html/body/div[1]/app-root/submission-history/div/ag-grid-angular/div/div[3]/div/div/div/div[2]/button[2]'
apply_year_filter = driver.find_element(By.XPATH, apply_year_filter_path)
apply_year_filter.click()

# purpose is to let used select the type of form now
'''
Possible string inputs: 
Form 1, Form 1F, Form 2, Form 2A, Form 3Q Electric, Form 3Q Gas, Form 6, Form 60, Form 6Q, Form 714
'''

# list of potential forms we can filter for
form_types = ['Form 1', 'Form 1F', 'Form 2', 'Form 2A', 'Form 3Q Elecrtric', 'Form 3Q Gas', 
              'Form 6', 'Form 60', 'Form 6Q', 'Form 714']

# finding form filter drop down menu
form_button_path = '/html/body/div[1]/app-root/submission-history/div/ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div/div[3]/div[3]/span'
form_button = driver.find_element(By.XPATH, form_button_path)
form_button.click()

# now we are inserting the form type we want to filter for
form_filter_input = ''
form_filter = driver.find_element(By.XPATH, form_filter_input)
form_filter.send_keys('Form 714')

# purpose is to click on the search icon to apply filter
apply_form_filter_path = '/html/body/div[1]/app-root/submission-history/div/ag-grid-angular/div/div[3]/div/div/set-filter/div/div[3]/div/mat-form-field/div/div[1]/div[2]'
apply_form_filter = driver.find_element(By.XPATH, apply_form_filter_path)
apply_form_filter.click()

# letting the webpage chill out for a bit to allow for the eforms site to load
# webpage loads in a little under 7 seconds so setting at 10 should be sufficient
time.sleep(15)

# closing the window of our loaded webpage
driver.quit()
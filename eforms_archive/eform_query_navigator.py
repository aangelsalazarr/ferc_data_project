import time
import io
import pandas as pd
import math
from datetime import date
import requests 


# selenium related tools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# importing sub functions
import eform_query_processor as eqp

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

#==============================================================================
# CHOOSE INPUTS TO RUN ON
#==============================================================================
choose_year = '2023'
choose_form = 'Form 714'



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
WebDriverWait(driver, 16).until(EC.presence_of_all_elements_located((By.XPATH, eform_tbl_row1)))

# letting the user know that the eform table has been identified
print('Table containing eforms is present (=')

# now we want to filter out by year
year_button_path = '/html/body/div/app-root/submission-history/div/ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div/div[4]/div[3]/span'
year_button = driver.find_element(By.XPATH, year_button_path)
year_button.click()

# now we want to input string value represetning year we would like to filter for year, e.g. 2024
year_filter_input = '/html/body/div/app-root/submission-history/div/ag-grid-angular/div/div[3]/div/div/div/div[1]/div[1]/div[1]/input'
year_filter = driver.find_element(By.XPATH, year_filter_input)
year_filter.send_keys(f'{choose_year}')

# purpose is to click apply filter on the year filter
apply_year_filter_path = '/html/body/div[1]/app-root/submission-history/div/ag-grid-angular/div/div[3]/div/div/div/div[2]/button[2]'
apply_year_filter = driver.find_element(By.XPATH, apply_year_filter_path)
apply_year_filter.click()

# list of potential forms we can filter for
form_types = ['Form 1', 'Form 1F', 'Form 2', 'Form 2A', 'Form 3Q Elecrtric', 'Form 3Q Gas', 
              'Form 6', 'Form 60', 'Form 6Q', 'Form 714']

# finding form filter drop down menu
form_button_path = '/html/body/div[1]/app-root/submission-history/div/ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div/div[3]/div[3]/span'
form_button = driver.find_element(By.XPATH, form_button_path)
form_button.click()

# now we are inserting the form type we want to filter for
form_filter_input = '//*[@id="textFilter"]'
form_filter = driver.find_element(By.XPATH, form_filter_input)
form_filter.send_keys(f'{choose_form}')

# purpose is to click on the search icon to apply filter
apply_form_filter_path = '/html/body/div[1]/app-root/submission-history/div/ag-grid-angular/div/div[3]/div/div/set-filter/div/div[3]/div/mat-form-field/div/div[1]/div[2]'
apply_form_filter = driver.find_element(By.XPATH, apply_form_filter_path)
apply_form_filter.click()

# now we begin the process of exporting the table of FERC 714 forms in order to filter out any redundancies
def grab_eform_tbl():
    '''
    purpose of this function is to grab table data within a ferc elibrary page and return as df
    '''

    # path to our table within the html code
    # as of now we assume that the table will exist... need to account for when there is not table
    grid_xpath = '//*[@id="myGrid"]'

    # get the HTML content of the table
    grid_element = driver.find_element(By.XPATH, grid_xpath)

    # extracting data from the agi grid
    data = grid_element.find_elements(By.CSS_SELECTOR, '.ag-row')
    col_headers = grid_element.find_elements(By.CSS_SELECTOR, '.ag-header-cell')

    # creating a list of dicts to represent the data
    rows = []
    for raw_element in data:
        raw_data = {}
        cells = raw_element.find_elements(By.CSS_SELECTOR, '.ag-cell')

        for i, cell in enumerate(cells):
            col_header = col_headers[i].text
            raw_data[col_header] = cell.text
        rows.append(raw_data)

    # dataframe of html table
    dataframe = pd.DataFrame(rows)

    # removing any empty rows
    dataframe = dataframe.dropna()

    return dataframe

# checking to see if we can successfully grabbed the table
#test_case = grab_eform_tbl()
#test_case.to_csv(f'process_check/{choose_year}_temp_eform_results.csv', index=False)


# given the total number of results, returns total number of results
def num_of_query_pages():
    '''
    returns total number of queries within the webpage
    '''
    # total results
    total_results = driver.find_element(By.CLASS_NAME, 
                                        'ag-paging-row-summary-panel')

    # string that looks like 1 - 100 of 814
    string = str(total_results.text)

    # splitting our string by spacing
    range_label_parts = string.split()

    # finding the index of "of"
    of_index = range_label_parts.index("of")

    # extract the numerical value after "of"
    total_results_found = range_label_parts[of_index + 1]

    # found results as an integer
    results_num = int(total_results_found)

    # divide by 100 queries and then round up to find total number of pages we 
    # have to iterate through
    total_pages = math.ceil(results_num / 11)

    return total_pages

# calculating how many pages we have
total_results_pages = num_of_query_pages()
print(f'Total number of pages: {total_results_pages}')

### now we want to iterate through each page and grab grid data

# first we are creating a master df
master_df = pd.DataFrame()

# iterate process of going through each page and grabbing each table
for page_num in range(1, total_results_pages+1):
    # printing out what page we are on
    print(f'Currently processing page number: {page_num}')

    # grabbing the table for the specific page
    temp_df = grab_eform_tbl()

    # checking out temp_df
    print(temp_df)

    # add to master df
    master_df = pd.concat([master_df, temp_df], ignore_index=True)

    # setting the page number where we want to extract info from
    results_page_num = driver.find_element(By.XPATH, 
                                        '/html/body/div[1]/app-root/submission-history/div/ag-grid-angular/div/div[2]/span[2]/div[3]/button')
    
    # if not on last page, then click
    if page_num < total_results_pages:
        results_page_num.click()

    else: 
        print("at the last page!")


# insert an if statement to filter out any non form 1s 
# the reason why have to do is because successful filter actually returns
# anything with a '1' in it
if choose_form == 'Form 1':
    # filtering to return only Form 1 forms
    master_df = master_df[master_df['Form'] == 'Form 1']
    print("Filtering out any non 'Form 1' forms!")

else: 
    # let user know all is well lol
    print('All is well, lad!')

# checking our master df 
print(master_df)


# creating a string of todays date
today = str(date.today())

# setting up the name of our main df export csv
eform_file_pull_name = 'eform_form_1'
master_df.to_csv(f'process_check/{eform_file_pull_name}_{today}_{choose_year}.csv', 
                 index=False)

# letting the webpage chill out for a bit to allow for the eforms site to load
# webpage loads in a little under 7 seconds so setting at 10 should be sufficient
time.sleep(10)

# closing the window of our loaded webpage
driver.quit()

# returning list of all filing ids
filing_ids_list = list(master_df['Filing ID'])
print(filing_ids_list)

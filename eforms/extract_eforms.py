import requests 
import time
import io
import pandas as pd
import math
from datetime import date

# selenium related tools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# other functions that will allow us to grab sub functions
import transform_eforms as teforms

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

def return_eforms(year: int, form_type = 'Form 714'):
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
    year_filter.send_keys(str(year))

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
    form_filter_input = '//*[@id="textFilter"]'
    form_filter = driver.find_element(By.XPATH, form_filter_input)
    form_filter.send_keys(str(form_type))

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
        '''
        iterate going through, changing the page number, and then grabbing the loaded table
        '''
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

    # letting the webpage chill out for a bit to allow for the eforms site to load
    time.sleep(15)

    # closing the window of our loaded webpage
    driver.quit()

    # returning the dataframe containing information 
    return master_df


# running return eforms function and then saving dataframe 
eforms_df = return_eforms(year=2023)

# eforms results list of filing ids
eforms_filing_ids = teforms.process_eform_data(init_dataframe=eforms_df)

# function that iterates through list to grab filings
def return_eform_filings(filing_ids: list, download_path=None):
    '''
    iterate through list and return files of data 
    provide list of filing ids and then also a string of where you would like to save files
    '''

    for filing_id in filing_ids:
        
        # setting up the download directory
        options = webdriver.ChromeOptions()

        # path of where we want to store our data
        prefs = {"download.default_directory": fr"{download_path}", 
                 'safebrowsing.enabled': "false"
                 }

        # adding options to our chrome driver
        options.add_experimental_option("prefs", prefs)

        # creating a chome session
        driver = webdriver.Chrome(options=options)

        # opening ferc library specific page
        driver.get(f'https://ecollection.ferc.gov/submissionDetails/{filing_id}')

        # allow the website to load for a little bit
        driver.implicitly_wait(10)

        # pulling data from the page to rename our file
        # want to name files as follows: {filing_entity}_ferc_714_{Quarter Period}{Year}.xml
        # an example: Electric Reliability Council of Texas, Inc._ferc_714_4Q2023.xml

        # grabbing company name
        company_name_path = '/html/body/div[1]/app-root/submission-detail/div/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div/div/div[2]'
        company_name = driver.find_element(By.XPATH, company_name_path)
        company_name_text = company_name.text

        # filing quarter period
        quarter_period_path = '/html/body/div[1]/app-root/submission-detail/div/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div/div/div[5]'
        quarter_period = driver.find_element(By.XPATH, quarter_period_path)
        quarter_period_text = quarter_period.text

        # year period
        year_path = '/html/body/div[1]/app-root/submission-detail/div/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div/div/div[4]'
        year = driver.find_element(By.XPATH, year_path)
        year_text = year.text

        # xml file name 
        xml_file_name = f'{company_name_text}_ferc_714_{quarter_period_text}{year_text}_{filing_id}.xml'
        print(xml_file_name)

        # xml download button types, third div is the change in value
        # button type A: /html/body/div[1]/app-root/submission-detail/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[1]
        # button type B: /html/body/div[1]/app-root/submission-detail/div/div[2]/div[1]/div[1]/table/tbody/tr[1]/td[1]

        # trying button path A first then B if all else fails
        xml_button_path_a = '/html/body/div[1]/app-root/submission-detail/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[1]'
        xml_button_path_b = '/html/body/div[1]/app-root/submission-detail/div/div[2]/div[1]/div[1]/table/tbody/tr[1]/td[1]'

        try:
            download_xml_button = driver.find_element(By.XPATH, xml_button_path_a)
            download_xml_button.click()

        except:
            download_xml_button = driver.find_element(By.XPATH, xml_button_path_b)
            download_xml_button.click()

        # let the website driver browser sleep/chill for a bit
        time.sleep(10)

        # closing the browser
        driver.quit()
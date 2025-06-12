import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import os

import time
import requests
import pandas as pd
import io
import math

import elibrary_query_processor as eqp

'''
Some info on the FERC Orders

1. FERC Order 1920, sub docket of public comment period stored under RM21-17
2. FERC Order 202023, sub docket of public comment period stored under RM 22-14
3. RM22-7: Applications for permits to site interstate electric transmission facilities

List of docket nums we thus want to pull....

docket_numbers = ['RM21-17', 'RM22-7', 'RM22-14']

'''


def return_elibrary_files(docket_num:str, save_path: str):

    # given the total number of results, returns total number of results
    def num_of_query_pages():
        '''
        returns total number of queries within the webpage

        docket examples: RM21-17, RM22-7, RM22-14
        save_path, where the elibrary files will be stored, 
        '''
        # total results
        total_results = driver.find_element(By.CLASS_NAME, 'mat-paginator-range-label')

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
        total_pages = math.ceil(results_num / 100)

        return total_pages


    def grab_elibrary_tbl():
        '''
        purpose of this function is to grab table data within a ferc elibrary page and return as df
        '''

        # path to our table within the html code
        # tbody = /html/body/app-root/html/body/div/main/app-docketsheet/table/tbody
        # tbl = //*[@id="tblRslt"]
        table_xpath = '//*[@id="tblRslt"]'

        # only shows up when a table doesn't have any results
        no_result = "noRslt"

        # asking webdrive to wait 5 sectonds or unitl the no result table is no longer present
        table_element = WebDriverWait(driver, 5).until_not(lambda x: x.find_element(By.ID, no_result).is_displayed())

        # get the HTML content of the table
        table_html = driver.find_element(By.XPATH, 
                                         table_xpath).get_attribute("outerHTML")

        # converting table html to a string format
        table_html = io.StringIO(table_html)

        # processing table html and converting into a pandas df
        data = pd.read_html(table_html)[0]

        # real df
        real_df = pd.DataFrame(data)

        return real_df


    # setting up the driver path
    driver_path = ''

    # creating a Chrome session
    driver = webdriver.Chrome()

    # opening ferc elibrary
    driver.get('https://elibrary.ferc.gov/eLibrary/search')

    # allow the website to load for a little
    driver.implicitly_wait(3)

    # desired value of the radio button that we want to press
    docket_value = "docket"

    # find all radio buttons using the mat radio button tag
    radio_buttons = driver.find_elements(By.TAG_NAME, "mat-radio-button")

    # loop through each radio button and look for the one matching value
    for button in radio_buttons: 
        if button.get_attribute("value") == docket_value:
            button.click()
            print(f"Selected radio button with value: {docket_value}")
            break

    # next we want to input the docket number in the docket number field
    enter_docket_num = driver.find_element(By.ID, "docketfield")

    # inputting the desired text into the field
    enter_docket_num.send_keys(docket_num)  ## change this whenever you want to shift between diff types of reports

    # now we want to click submit to load results
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()

    ## TEST CASE
    # test_df = grab_elibrary_tbl()
    # print(test_df)

    # queries master df
    master_df = pd.DataFrame()

    # calculating how many pages we have to iterate through
    total_results_pages = num_of_query_pages()
    print(f'total number of pages we have to iterate through: {total_results_pages}')

    # iterate process of going through each page and grabbing each table
    for page_num in range(0, total_results_pages):
        '''
        iterate going through, changing the page number, and then grabbing the loaded table
        '''
        print(f'Currently processing page number: {page_num}')

        # setting the page number where we want to extract info from
        results_page_num = driver.find_element(By.XPATH, 
                                            '/html/body/app-root/html/body/div/main/app-docketsheet/table/caption/mat-toolbar/div/mat-form-field/div/div[1]/div/mat-select/div')
        
        results_page_num.click()

        # wait for options to be available
        wait = WebDriverWait(driver, 10)
        options = wait.until(EC.presence_of_all_elements_located((By.XPATH, 
                                                                "//mat-option")))

        # iterate through options and select the desired one
        for option in options: 
            if option.text == f'{page_num+1}':
                option.click()

        # grabbing the table for the specific page
        temp_df = grab_elibrary_tbl()

        # checking out temp_df
        print(temp_df)

        # add to master df
        master_df = pd.concat([master_df, temp_df], ignore_index=True)

    # if a directory to store file does not exist then create it
    os.makedirs(f'{save_path}', exist_ok=True)
    master_df.to_csv(f'{save_path}/{docket_num}_all_queries.csv', index=False)

    # making website chill for a bit
    time.sleep(5)

    # closing the driver window
    driver.quit()

    # returning the master df so it can be used
    return master_df


#####################TEST######################
# grabbing the master df
main_df = return_elibrary_files(docket_num='RM10-23', 
                                save_path='elibrary/process_check')


# process main df to return list of accession codes
list_of_accessions = eqp.queries_filter(dataframe=main_df, phrase="Comments", 
                                        save_folder='elibrary/process_check', 
                                        docket_num='RM10-23')

# iterate through accession list and return files
eqp.return_accession_files(accession_codes=list_of_accessions, docket_num="RM10-23")
# selenium related tools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd
import os

# importing base functions
import eforms_base_functions as eforms_bfuncs

# function that iterates through list to grab filings
def return_eform_filings(filing_ids: list, date_of_files: str, form_type='form_714', 
                         download_path=None, minimize_browser=True):
    '''
    iterate through list and return files of data 
    provide list of filing ids and then also a string of where you would like to save files

    form_type default is form_714, please change if this is not the case!!!
    '''

    # if no download path is saved then assume we should save in a 'form_714 files
    if download_path is None: 
        # in this case create a folder where we will be saving our files
        os.makedirs(f'eforms/{form_type}_{date_of_files}', exist_ok=True)
        download_path = f'{str(os.getcwd())}/eforms/{form_type}_{date_of_files}'

    else: 
        print(f'Download Path Defined As: {download_path}')


    for filing_id in filing_ids:
        
        # setting up the download directory
        options = webdriver.ChromeOptions()
        
        # disable pop up blocking and notifications
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')

        # path of where we want to store our data
        prefs = {"download.default_directory": fr"{download_path}", 
                 'safebrowsing.enabled': "false"
                 }

        # adding options to our chrome driver
        options.add_experimental_option("prefs", prefs)

        # creating a chome session
        driver = webdriver.Chrome(options=options)

        # minimizing window
        if minimize_browser: 
            driver.minimize_window()

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


'''
# we are defining which eforms df we are referencing to pull data
eforms_df = pd.read_csv('eforms/process_check/Form 714_2025-05-24.csv')
files_dated = eforms_df['Year'][0]

# defining which eform table list we want to pull from 
eform_filing_ids = eforms_bfuncs.process_eform_data(init_dataframe=eforms_df)

# now we can call the function that will iterate through and grab all files referenced
return_eform_filings(filing_ids=eform_filing_ids, date_of_files=files_dated)
'''
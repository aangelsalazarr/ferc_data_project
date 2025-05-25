from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import pandas as pd

import os


# test accession codes
test_codes = ['20211012-5620', '20211012-5638']


def queries_filter(dataframe, phrase, save_folder, docket_num, save_pls=True):
    '''
    purpose is to filter by checking whether the description contains a set of strings
    included the ability to save for future once we have everything set up
    '''

    # cleaning up the accession number to begin with
    dataframe['Accession_Num'] = dataframe['Accession'].str.split().str[0]

    # processed query
    dataframe_filtered = dataframe[dataframe['Description'].str.contains(f'{phrase}', 
                                                                         case=False)]
    
    # resetting our index
    dataframe_filtered = dataframe_filtered.reset_index()

    # converting the accession new column into a list to extract
    accessions_list = list(dataframe_filtered['Accession_Num'])

    # checking to see if user wants to save data
    if save_pls == True:
        # saves filtered query df
        dataframe_filtered.to_csv(f'{save_folder}/{docket_num}_filtered_queries.csv', index=False)

    else: 
        print('User has chosen to not save this data!')

    return accessions_list


def return_accession_files(accession_codes: list, docket_num: str, download_path=None, minimize_browser=True):
    '''
    iterate through a list of accessions and download files within the data 
    portal
    '''

    # if no download path is saved then assume we should save in a 'form_714 files
    if download_path is None: 
        # in this case create a folder where we will be saving our files
        os.makedirs(f'elibrary/{docket_num}_files', exist_ok=True)
        download_path = f'{str(os.getcwd())}/elibrary/{docket_num}_files'

    else: 
        print(f'Download Path Defined As: {download_path}')

    for accession in accession_codes:

        # setting up the download directory changes
        options = webdriver.ChromeOptions()

        # path of where we want to reroute downloads to 
        prefs = {'download.default_directory': fr'{download_path}', 
                 'safebrowsing.enabled':'false'
                 }

        # adding options to our chrome driver
        options.add_experimental_option('prefs', prefs)

        # setting up the driver path
        driver_path = ''

        # creating a chrome session 
        driver = webdriver.Chrome(options=options)

        # minimizing window
        if minimize_browser: 
            driver.minimize_window()

        # opening ferc elibrary to the specific submission webpage
        driver.get(f"https://elibrary.ferc.gov/eLibrary/filelist?accession_number={accession}")

        # alow the website to load for a little bit
        driver.implicitly_wait(10)      

        # download all button 
        download_pdf = driver.find_element(By.XPATH, 
                                           '/html/body/app-root/html/body/div/main/app-filelist/section/div[1]/table/tbody/tr/td[1]')
        download_pdf.click()

        # making the website chill for a bit
        time.sleep(3)

        # closing the driver window now
        driver.quit()


# a quick check to make sure it works -- it does (:
## return_accession_files(accession_codes=test_codes)
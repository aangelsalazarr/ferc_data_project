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


# test accession codes
test_codes = ['20211012-5620', '20211012-5638']


def return_accession_files(accession_codes: list, download_path=None):
    '''
    iterate through a list of accessions and download files within the data 
    portal
    '''

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
return_accession_files(accession_codes=test_codes)
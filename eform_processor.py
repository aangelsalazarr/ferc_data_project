from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium
import time
from webdriver_manager.chrome import ChromeDriverManager


# filing id test list
filing_id_test_list = ['192310', '181864']

# function that iterates through list to grab filings
def return_eform_filings(filing_ids: list):
    '''
    iterate through list and return files of data 
    '''

    for filing_id in filing_ids:

        # setting up our driver path
        driver_path = ''

        # creating a chome session
        driver = webdriver.Chrome()

        # opening ferc library specific page
        driver.get(f'https://ecollection.ferc.gov/submissionDetails/{filing_id}')

        # allow the website to load for a little bit
        driver.implicitly_wait(10)

        # xml download button
        xml_button_path = '/html/body/div[1]/app-root/submission-detail/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[1]/span'
        download_xml_button = driver.find_element(By.XPATH, xml_button_path)
        download_xml_button.click()

        # let the website driver browser sleep/chill for a bit
        time.sleep(7)

        # closing the browser
        driver.quit()
        
# test case
return_eform_filings(filing_ids=filing_id_test_list)
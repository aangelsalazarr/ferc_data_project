from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options

# filing id test list
filing_id_test_list = ['192310', '181864']

# function that iterates through list to grab filings
def return_eform_filings(filing_ids: list):
    '''
    iterate through list and return files of data 
    provide list of filing ids and then also a string of where you would like to save files
    '''

    for filing_id in filing_ids:
        
        # setting up the download directory
        options = webdriver.ChromeOptions()

        # path of where we want to store our data
        prefs = {"download.default_directory": r"C:\Users\aange\OneDrive\Desktop\Personal Python Projects\ferc_data_project\ferc_714_xml_files"}

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
        xml_file_name = f'{company_name_text}_ferc_714_{quarter_period_text}{year_text}.xml'
        print(xml_file_name)

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
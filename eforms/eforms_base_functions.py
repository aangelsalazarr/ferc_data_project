'''
AS: uploading all the code and here is a quick snipper of its purpose.
here we will store functions that transform any of the data we are working with
'''
from datetime import date
import pandas as pd

def process_eform_data(init_dataframe: object, 
                       folder_path=None,
                       save_pls = False):
    '''
    given input of a dataframe, applied needed changes to make sure it can be 
    fed into the eform query processor
    '''

    # setting up data string to apply to when we would like to save our data
    today = str(date.today())

    # return list of the filing ids that are grabbed from the eform grabber
    filing_id_list = list(init_dataframe['Filing ID'])

    # saving the dataframe into provided path
    if save_pls == True: 
        '''
        in this case we would like to save our dataframe as a csv
        user needs to supply folder path of where this data will be saved
        '''
        print('User has selected to save df! (= ')
        init_dataframe.to_csv(f'{folder_path}/eform_filtered_data_{today}.csv', index=False)

    else:
        '''
        in this case we will not be saving our dataframe as a csv
        '''
        print('User did not select to save df =()')

    # returning a list of filing ids in case user wanted to just copy and paste
    print("Here is your list of Filing IDs: ")
    print(filing_id_list)

    return filing_id_list
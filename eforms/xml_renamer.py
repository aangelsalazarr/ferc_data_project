import pandas as pd
import os

'''
The purpose of this python script is to iterate through specific filings and 
rename files appropriately, providing a unique name per file. 

'''

# =================
# retrieve file creation time stamp
#==================
def retrieve_creation_timestamp(item_file: str, dir_path: str):
    '''
    Args:

    item_file -> give file name and function returns when file was created
    dir_path -> directory path of where the file is located
    '''
    item_path = os.path.join(dir_path, item_file)

    return os.path.getctime(item_path)


# =================
# sorting directory
#==================
def sort_directory(sort_by: str, dir_path: str):
    '''
    Args: 

    sort_by -> allows user to decide whether they would like to sort by 
                date or by name
    dir_path -> path of directory where we will be storing renamed files
    '''
    # purpose is to return the time the file was created
    def get_creation_timestamp(item):
        item_path = os.path.join(dir_path, item)
        return os.path.getctime(item_path)

    # save a list of the files within specific directory
    items = os.listdir(dir_path)

    if sort_by == 'date':
        # sorting by date
        print('sorting files in directory by creation date!')

        # sorting items from oldest to newest
        sorted_items = sorted(items, 
                              key=get_creation_timestamp)
        
        return sorted_items

    elif sort_by == 'name':
        # sorting by name
        print('sorting files in the directory by name')

        # sorting items by name
        sorted_items = 'blank for now'

        return sorted_items

    else: 
        # user did not set sorty by name or date
        print('please redefine how you would like to sort!')


# =================
# cleaning xml file initial refnames
#==================

def clean_initial_refname(refname_list: list):
    '''
    Arge
    refname_list -> list of unique name non processed
    '''
    # final_refname
    final_refnames = []

    for refname in refname_list:
        # check for instances where these exist and replace with _
        iteration_1 = refname.replace("/", "_")
        iteration_2 = iteration_1.replace(",", "_")
        iteration_3 = iteration_2.replace(" ", "_")
        iteration_4 = iteration_3.replace(".", "_")
        final_iteration = iteration_4.replace(":", "_")
        final_refnames.append(final_iteration)

    return final_refnames


# =================
# xml rename, or also known as initial refname
#==================
def refname_xml_base(dframe: object):
    '''
    in essence, go through df and set up framework for the renaming of xml files grabbed
    '''
    # a finalized list of the renamed xml names
    renamed_xmls = []

    # columns to combine and combined strings list
    columns_to_combine = ['Form', 'Year', 'Company', 'Period', 'Date/Time', 'Filing ID']

    # combined strings
    for index, row in dframe.iterrows():

        # for each row in our dataframe we are combining select col values
        combined_string = ' '.join(row[columns_to_combine].astype(str))

        # in essence now changing all sub text into underscores
        final_string = clean_initial_refname(refname_list=list(combined_string))

        # combined final string where we have converted all sub elements in our words
        f_string = ''.join([str(item) for item in final_string])

        # printing combined string to see what's up
        renamed_xmls.append(f_string)
    
    return renamed_xmls

    
# =================
# renaming all files xbrl or xml within directory
#==================
def rename_all_files(xml_df: object, dir_path: str, sort_by = 'date'):

    '''
    now we will first iterate through xml df, grab rows of data to set up a unique file name
    and then rename the file to that name

    xml_df = df we used to pull the files from the ferc website
    sort_by = set to 'date' default but can also be set to 'name'
    dir_path = path of where the files downloaded is at....
    '''
    print('here is what we are working with: ')
    print(f'inputted df: {xml_df}')
    print(f'dir_path: {dir_path}')
    print('\n')

    # first, we are defining the directory path where we will be making the changes
    files_list = sort_directory(sort_by=sort_by, dir_path=dir_path)
    print(files_list)

    # renaming xml files
    temp_xmls = refname_xml_base(dframe=xml_df)
    print(temp_xmls)  

    # now we want to iterate through each file and rename it
    for file in files_list: 
        # true file path
        true_file_path = f'{dir_path}/{file}'
        print(true_file_path)

        # new name
        print(f'new file name: {temp_xmls[file.index(str(file))]}')

        # rename file by grabbing location of the 'file' element
        new_fpath = os.rename(f'{true_file_path}', 
                              f'{dir_path}/{temp_xmls[files_list.index(str(file))]}.xml')
        
    print(f'Success Renaming Files Located at: {dir_path}')
        


# we first need to load in the dataframe we used to pull our data
xml_df_test = pd.read_csv('eforms/process_check/Form 714_2025-05-23.csv')
dir_path_test = 'eforms/form_714_2024'

rename_all_files(xml_df=xml_df_test, dir_path=dir_path_test)


from xml.etree import ElementTree as ET
import os

def create_xml_filename(filepath):

    # filepath
    basepath = filepath

    # importing the treeee
    tree = ET.parse(basepath)
    root = tree.getroot()

    # balancing authority area name accessing via xpath
    baan = tree.getroot().find('ferc:BalancingAuthorityAreaName', 
                                namespaces={'ferc': 'http://ferc.gov/form/2024-04-01/ferc'})

    # replacing spaces with underscores
    baan_underscored = baan.text.replace(" ", "_")

    # Find the context element
    context = root.find('xbrli:context', 
                        namespaces={'xbrli':'http://www.xbrl.org/2003/instance'})

    # Find the period element
    period = context.find('xbrli:period', 
                        namespaces={'xbrli':'http://www.xbrl.org/2003/instance'})

    # Access the endDate element text
    end_date = period.find('xbrli:endDate', 
                        namespaces={'xbrli':'http://www.xbrl.org/2003/instance'}).text

    # end date underscored
    end_date_underscored = end_date.replace("-", "_")

    # accessing the certifying date element
    certif_date = tree.getroot().find('ferc:CertifyingOfficialDate', 
                              namespaces={'ferc': 'http://ferc.gov/form/2024-04-01/ferc'})
    
    # certification official date underscored
    certif_date_underscored = certif_date.text.replace("-", "_")


    # final filename
    final_filename = f'ferc_714_{baan_underscored}_{certif_date_underscored}'

    return final_filename

# path to file we are testing
# test_file = "ferc_714_xml_files/spp-20231231.xbrl"
#spp_file = create_xml_filename(filepath=test_file)
#print(spp_file)

def change_xbrl_xml_fname(folder_path, file_path, old_fname):
    '''
    Args: 
    folder_path: this is where the file exists within a given folder
    file_path: this is the name of the file itself 
    old_fname: moreso thought of as the original name
    '''

    # let user know that the file is being processed
    print(f'Processing file: {file_path}')

    try:
        '''
        trying to change the name and accounting for duplicate names
        '''
        # updated file path using context from the file itself
        updated_filepath = create_xml_filename(file)


    except Exception as e:

        '''
        in the case that we are getting an error in our function application
        '''

        print(f'Error: {e}')

# function that renames a file...
def process_xbrl_file(file_path, old_fname, folder_path):

    '''
    if rename yields error because file with same name exists, then just 
    '''

    # Your function to process the XBRL file
    print(f"Processing file: {file_path}")
    try:
        # grabbing xml file rename 
        created_fname = create_xml_filename(filepath=file_path)

        # setting up the true file path
        true_file_path = f'{folder_path}/{created_fname}'

        # allows us to number file names that will end up being the same
        int = 1

        # renaming file
        new_file_path = os.rename(old_fname, f'{true_file_path}')

        # if filepath already exists, then just add v{int} to the end
        while os.path.exists(new_file_path):
            new_file_path = os.rename(old_fname, f'{true_file_path}_v{str(int)}')
            int += 1
    
    except Exception as e:
        print(f'Error: {e}')


# now the real thing beginning with our folder path
folderpath = 'ferc_714_xml_files'

# get a list of all files in the folder
files = os.listdir(folderpath)

# iterating through eachfile and renaming it
for file in files: 

    # check if file has a xbrl extenstion
    if file.endswith('.xbrl'):
        
        # in essence, join folder path and specific file so it can be 
        # correctly referenced
        file_path= os.path.join(folderpath, file)
        
        #process the given file
        process_xbrl_file(file_path=file_path, 
                          old_fname=file_path, 
                          folder_path=folderpath)
        

    if file.endswith('.xml'):

        file_path(os.path.join(folderpath, file))

        # processing file to rename it accordingly
        process_xbrl_file(file_path=file_path, 
                          old_fname=file_path, 
                          folder_path=folderpath)
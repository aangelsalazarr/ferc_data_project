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

# function that renames a file...
def process_xbrl_file(file_path, old_fname, folder_path):

    # Your function to process the XBRL file
    print(f"Processing file: {file_path}")

    # grabbing xml file rename 
    created_fname = create_xml_filename(filepath=file_path)

    # setting up the true file path
    true_file_path = f'{folder_path}/{created_fname}'

    # renaming file
    os.rename(old_fname, true_file_path)


# now the real thing beginning with our folder path
folderpath = 'ferc_714_xml_files'

# get a list of all files in the folder
files = os.listdir(folderpath)

# iterating through eachfile and renaming it
for file in files: 

    # check if file has a xbrl extenstion
    if file.endswith('.xbrl'):
        file_path= os.path.join(folderpath, file)
        process_xbrl_file(file_path=file_path, 
                          old_fname=file_path, 
                          folder_path=folderpath)
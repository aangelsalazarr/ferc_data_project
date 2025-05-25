# FERC Data Projects
Python Scripts Facilitating the Navigation of FERC Data. This project was directly inspired by a report I read a few years ago titled [The Era of Flat Power Demand is Over](https://gridstrategiesllc.com/wp-content/uploads/2023/12/National-Load-Growth-Report-2023.pdf) by GridStrategies (Authors: John D. Wilson and Zach Zimmerman).

The main purpose of this project is to automate the retrieval, storing and analysis of FERC 714 Form Data. More specifically, I am interested in parsing through and grabbing forecast related data from this report. 

Moreover, we would like to automate a process of grabing files from the FERC E-Library. 

# Issue & Solution
The FERC website, while very *fresh*, makes it extremely difficult to access public data. Moreover, there currently exists no easy to use tool that can help an individual obtain FERC 714 data in an aggregate format that can then be analyzed. The issue I am trying to solve is simple: can i reduce labor hours and attention needed in acquiring as much FERC 714 forms as possible? 

Update: [Catalyst Cooperative](https://github.com/catalyst-cooperative/pudl) is a community of individuals working towards building open source tools that can automate and extract information from a myriad of public energy data sources. For context, this is the same entity that processed the data used in the aforementioned report that served as an inspiration for this project! 

# FERC EFORM SCRIPT TUTORIAL
1. Run [Extract EForms Script](eforms/extract_eforms_available.py) to obtain a datatable of files that can be grabbed.

```python
# we are asking function to pull 2024 dated FERC Form 714 Files
eforms_df = return_eforms(year=2024, form_type='Form 714')

# eforms results list of filing ids
eforms_filing_ids =      eform_bfuncs.process_eform_data(init_dataframe=eforms_df) 
```
2. Run [Pull EForms Script](eforms/pull_eforms_available.py) to iterated through generated data table and save files in order.

```Python
# we are defining which eforms data table we are referencing to pull files
eforms_df = pd.read_csv('eforms/process_check/Form 714_2025-05-23.csv')

# this functions pulls date of filings (useful later)
files_dated = eforms_df['Year'][0]

# defining which eform table list we want to pull from 
eform_filing_ids = eforms_bfuncs.process_eform_data(init_dataframe=eforms_df)

# now we can call the function that will iterate through and grab all files referenced
return_eform_filings(filing_ids=eform_filing_ids, date_of_files=files_dated)
```

3. Run [File Renamer Script](eforms/xml_renamer.py) to iterated through each file pulled and rename appropriately. Most importantly this process includes datetime submission of file which will be important when cleaning up our file directory. 

```Python
# we first need to load in the dataframe we used to pull our data
xml_df_test = pd.read_csv('eforms/process_check/Form 714_2025-05-23.csv')

# we also need to define path of where files exist
dir_path_test = 'eforms/form_714_2024'

rename_all_files(xml_df=xml_df_test, dir_path=dir_path_test)
```
4. Datatables stored in process_check and Form 714 Files stored in form_714_2021

**There you have it!** We have successfully pulled *ALL* Form 714s from the FERC website for the specified year. 

# FERC ELibrary Tutorial
1. Run [ELibrary Query Navigator](elibrary/elibrary_query_navigator.py), which references [ELibrary Query Processor](elibrary/elibrary_query_processor.py). 

```Python
# creating main df, data table containing all files for RM22-7
main_df = return_elibrary_files(docket_num='RM22-7',
save_path='elibrary/process_check')

# process main df to return list of accession codes that have description including the phrase "Comments" 
list_of_accessions = eqp.queries_filter(dataframe=main_df, phrase="Comments", save_folder='elibrary/process_check', docket_num='RM22-7')

# iterate through accession list and return files
eqp.return_accession_files(accession_codes=list_of_accessions, docket_num="RM22-7")
```
2. Data tables stored in process_check and files are stored in RM22-7_files directory

# Components
### FERC Forms 
We will specifically be focused on FERF Form 714. For now we just want to grab the xml files, iterate through each file to categorize it by name and report date, and then go through and see if we can unify reports to view changes in 10 year forecast data by each entity that files this report. 

Ferc 714: Annual Electric Balancing Authority Area and Planning Area Report. Collects the following forecast data:
- Annual Peak Demand Forecasts (10 Years)
- Monthly Peak Demand Forecasts
- Energy Usage Forecasts
- Generation Adequacy Assessments
- Transmission Planning Data

[FERC 714 Summary Homepage](https://www.ferc.gov/industries-data/electric/general-information/electric-industry-forms/form-no-714-annual-electric/overview)


### FERC E-Library
We will specifically be focused on grabbing public comment files for Order 1920 and 2023. See below for summaries:

[FERC E-Library Homepage](https://elibrary.ferc.gov/eLibrary/search)

[FERC Ruling 2023](https://www.ferc.gov/explainer-interconnection-final-rule-2023-A): a landmark ruling to modernize the interconnection process for new generation facilities seeking to connect to the power grid. 
- technically there is 2023-A whcih is an amendment and clarificatino on order 2023
- order highlights that one of the most important aspects of the interconnection process relates to the technical studies associated with grid reliability and project implentation and connection to the grid. 
- In Order No. 2023, FERC required that transmission providers study proposed generating facilities in groups or clusters, rather than studying each individually or serially.

[FERC Ruling 1920](https://www.ferc.gov/news-events/news/ferc-strengthens-order-no-1920-expanded-state-provisions): requires transmission providers to conduct long-term planning of regional transmission facilities over 20-year time horizon to anticipate future needs and to determine how to pay for those tranmission facilities. 
- technically there exists a 1920-A which is an amendment to FERC ruling 1920. 




# Packages Required
- selenium
- pandas (or polars)
- time
- requests
- datetime
- math

## Windows 11 --> MacOS Transfer
If you initially developed any code on a windows laptop and then cloned said repository with code in a macbook here are some steps you may need to take...
1. navigate to your project directory: cd ferc_data_project
2. create a virtual environment, here is where we will be adding packages: python -m venv venv
3. activate the virtual environment: source venv/bin/activate
4. now you can install packages into the environment so that code will run!


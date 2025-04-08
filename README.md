# FERC Data Projects
Python Scripts Facilitating the Navigation of FERC Data. This project was directly inspired by a report I read a few years ago titled [The Era of Flat Power Demand is Over](https://gridstrategiesllc.com/wp-content/uploads/2023/12/National-Load-Growth-Report-2023.pdf) by GridStrategies (Authors: John D. Wilson and Zach Zimmerman).

The main purpose of this project is to automate the retrieval, storing and analysis of FERC 714 Form Data. More specifically, I am interested in parsing through and grabbing forecast related data. 

# Issue & Solution
The FERC website, while very *fresh*, makes it extremely difficult to access public data. Moreover, there currently exists no easy to use tool that can help an individual obtain FERC 714 data in an aggregate format that can then be analyzed. The issue I am trying to solve is simple: can i reduce labor hours and attention needed in acquiring as much FERC 714 forms as possible? 

Update: [Catalyst Cooperative](https://github.com/catalyst-cooperative/pudl) is a community of individuals working towards building open source tools that can automate and extract information from a myriad of public energy data sources. For context, this is the same entity that processed the data used in the aforementioned report that served as an inspiration for this project! 

# Notebooks
1. FERC 714 Data Acquisition and Visualization
2. FERC E-Library Order 2023/1920 Public Comment File Acquisition

# Skills Needed/Developed
- Ability to  parse through XML Fles
- Ability to code a webcrawler to automate the navigation of websites

# Components
### FERC Forms 
We will specifically be focused on FERF Form 714.

Ferc 714: Annual Electric Balancing Authority Area and Planning Area Report. Collects the following forecast data:
- Annual Peak Demand Forecasts (10 Years)
- Monthly Peak Demand Forecasts
- Eneergy Usage Forecasts
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


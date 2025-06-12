from datetime import date, datetime, timedelta

# pj functions
import eforms_base_functions as eform_bfuncs
import extract_eforms_available as eea

# running return eforms function and then saving dataframe 
eforms_df = eea.return_eforms(year=2023, form_type='Form 714')

# eforms results list of filing ids
eforms_filing_ids = eform_bfuncs.process_eform_data(init_dataframe=eforms_df)

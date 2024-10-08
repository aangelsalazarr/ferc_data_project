import eform_query_processor as eqp

# list of all 2023 files
ferc_714_2023_list = ['192310', '192309', '192306', '192277', 
                      '182167', '182066', '181984', '181976', 
                      '181968', '181934', '181864', '181824', 
                      '181790', '181649', '181639', '181638', 
                      '181636', '181590', '181574', '181569', 
                      '181568', '181564', '181559', '181555', 
                      '181554', '181540', '181532', '181531', 
                      '181517', '181513', '181512', '181511', 
                      '181508', '181486', '181484', '181483', 
                      '181477', '181475', '181466', '181436', 
                      '181434', '181431', '181425', '181413', 
                      '181401', '181400', '181399', '181394', 
                      '181392', '181386', '181380', '181378', 
                      '181375', '181370', '181354', '181350', 
                      '181340', '181339', '181319', '181309', 
                      '181305', '181294', '181288', '181282', 
                      '181267', '181233', '181211', '181199', 
                      '181179', '181160', '181109', '181098', 
                      '181090', '181086', '181065', '181057', 
                      '181056', '181031', '181030', '181029', 
                      '181021', '181019', '181018', '180996', 
                      '180972', '180958', '180952', '180929', 
                      '180927', '180926', '180923', '180888', 
                      '180884', '180857', '180840', '180799', 
                      '170758', '170745', '170743', '170698', 
                      '170692', '170673', '170545', '170377', 
                      '170367', '170346', '170312', '170307', 
                      '170289', '170287', '170284', '170265', 
                      '170253', '170247', '170214', '170208', 
                      '170199', '170178', '170154', '170140', 
                      '170132', '170129', '170111', '170110', 
                      '170104', '170101', '170083', '170079', 
                      '170060', '170046', '170045', '170044', 
                      '170042', '170028', '170022', '170020', 
                      '169957', '169912', '169906', '169875', 
                      '169871', '169863', '169810', '169794', 
                      '169777', '169760', '169702', '169658', 
                      '169489', '168752', '147627', '147324', 
                      '147056']

# testing to see where the issue lies
eqp.return_eform_filings(filing_ids=ferc_714_2023_list)


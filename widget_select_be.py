import pandas as pd
import functions

############# подготовка данных для чек-листа Бизнес-единица #####################

def be_select_data():
  full_eo_list = functions.full_eo_list_func()
  be_columns = full_eo_list.groupby(['level_1', 'level_1_description'])

  be_checklist_data = []
  be_checklist_values = []
  for be in be_list:
      dict_temp = {}
      dict_temp['label'] = be
      dict_temp['value'] = row['eo_class_code']
      eo_class_checklist_data.append(dict_temp)
      eo_class_values.append(row['eo_class_code'])
  return eo_class_checklist_data, eo_class_values
  
  print(be_list)
  
be_select_data()
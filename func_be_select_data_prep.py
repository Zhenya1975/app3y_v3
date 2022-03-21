import pandas as pd
import initial_values

def be_select_data_prep():
  ktg_by_month_data_df = pd.read_csv('data/ktg_by_month_data_df.csv', decimal = ",")
  be_list = list(set(ktg_by_month_data_df['level_1_description']))
  be_checklist_data = []
  be_values = be_list
  for be in be_list:
    dict_temp = {}
    dict_temp['label'] = be
    dict_temp['value'] = be
    be_checklist_data.append(dict_temp)
 
  return be_checklist_data, be_values


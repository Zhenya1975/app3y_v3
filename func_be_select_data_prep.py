import pandas as pd
import initial_values
import json

def be_select_data_prep():
  with open('saved_filters.json', 'r') as openfile:
    # Reading from json file
    saved_filters_dict = json.load(openfile)
  # print("saved_filters_dict", saved_filters_dict)
  
  ktg_by_month_data_df = pd.read_csv('data/ktg_by_month_data_df.csv', decimal = ",")
  be_list = list(set(ktg_by_month_data_df['level_1']))
 
  level_1_df = pd.read_csv('data/level_1.csv')
  level_1_df = level_1_df.loc[level_1_df['level_1'].isin(be_list)]
  be_checklist_data = []

  be_values_total = []
  for index, row in level_1_df.iterrows():
    dict_temp = {}
    level_1_code = row['level_1']
    level_1_description = row['level_1_description']
    dict_temp['label'] = level_1_description
    dict_temp['value'] = level_1_code
    be_checklist_data.append(dict_temp)
    be_values_total.append(level_1_code)
  
  # print("be_value", be_value)  
  
  
     
  # записываем в json
  # with open("saved_filters.json", "w") as jsonFile:
  #  json.dump(saved_filters_dict, jsonFile)
  # print(be_checklist_data)
  be_values = saved_filters_dict['filter_be']
  # print("сохраненный фильтр", saved_filters_dict['filter_be'])
  return be_checklist_data, be_values

# be_select_data_prep()


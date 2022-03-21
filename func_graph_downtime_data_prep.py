import pandas as pd
import initial_values
import functions

def graph_downtime_data_prep(be_list_for_dataframes_filtering):
  
  ktg_by_month_data_df = functions.ktg_data_reading()
  ktg_by_month_data_df = ktg_by_month_data_df.loc[ktg_by_month_data_df['level_1'].isin(be_list_for_dataframes_filtering)]
  ktg_graph_data = ktg_by_month_data_df.groupby(['month_year'], as_index=False)['downtime'].sum()
  
  period_dict = initial_values.period_dict
    
  period_sort_index = initial_values.period_sort_index
  
  ktg_graph_data['period'] = ktg_graph_data['month_year'].map(period_dict).astype(str)
  
  ktg_graph_data['period_sort_index'] = ktg_graph_data['month_year'].map(period_sort_index)
  ktg_graph_data.sort_values(by='period_sort_index', inplace = True)
  ktg_graph_data['downtime'] = ktg_graph_data['downtime'].astype(int)
  # ktg_graph_data['downtime'] = ktg_graph_data['downtime'].apply(lambda x: round(x, 0))
  
  ktg_graph_data.rename(columns={'period': 'Период', 'downtime': "Запланированный простой, час"}, inplace=True)
  ktg_graph_data = ktg_graph_data.loc[:, ['Период', 'Запланированный простой, час']]
  ktg_graph_data.to_csv('widget_data/downtime_graph_data.csv', index = False)
  return ktg_graph_data
# graph_downtime_data_prep()
import pandas as pd
import plotly.graph_objects as go
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

import initial_values
import functions
import json

# select the Bootstrap stylesheet2 and figure template2 for the theme toggle here:
# template_theme1 = "sketchy"
template_theme1 = "flatly"
template_theme2 = "darkly"
# url_theme1 = dbc.themes.SKETCHY
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

templates = [
    "bootstrap",
    "minty",
    "pulse",
    "flatly",
    "quartz",
    "cyborg",
    "darkly",
    "vapor",
    "sandstone"
]

load_figure_template(templates)

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"
)
 
################# График простоев по месяцам за три года ###############################
def widgets_data(theme_selector, be_list_for_dataframes_filtering):
  """Данные для графиков"""

  ########################### ГРАФИК ПРОСТОЕВ ###############################
  # данные о простоях и календарном фонде
  ktg_by_month_data = pd.read_csv('widget_data/ktg_by_month_data_df.csv', decimal = ",")
  # режем по фильтру
  
  
  
  ktg_by_month_data_filtered = ktg_by_month_data.loc[ktg_by_month_data['level_1'].isin(be_list_for_dataframes_filtering)]
  ktg_by_month_data_filtered = ktg_by_month_data_filtered.copy()
  ktg_by_month_data_filtered['month_year'] = ktg_by_month_data_filtered['month'].astype(str) + "_" + ktg_by_month_data_filtered['year'].astype(str)
  
  # ktg_by_month_data_filtered.loc[:, ['month_year']] = ktg_by_month_data_filtered.loc[:, ['month']].astype(str) + "_" + ktg_by_month_data_filtered.loc[:, ['year']].astype(str)

  ########### ГРУППИРОВКА  #####################
  downtime_ktg_graph_data = ktg_by_month_data_filtered.groupby(['month_year', 'eo_model_name'], as_index=False)[['calendar_fond','downtime']].sum()

  
  downtime_ktg_graph_data['ktg'] = (downtime_ktg_graph_data['calendar_fond'] - downtime_ktg_graph_data['downtime']) / downtime_ktg_graph_data['calendar_fond']
  downtime_ktg_graph_data['downtime'] = downtime_ktg_graph_data['downtime'].apply(lambda x: round(x, 0))
  downtime_ktg_graph_data['ktg'] = downtime_ktg_graph_data['ktg'].apply(lambda x: round(x, 2))
  period_dict = initial_values.period_dict
    
  period_sort_index = initial_values.period_sort_index
  
  downtime_ktg_graph_data['period'] = downtime_ktg_graph_data['month_year'].map(period_dict).astype(str)
  
  downtime_ktg_graph_data['period_sort_index'] = downtime_ktg_graph_data['month_year'].map(period_sort_index)
  downtime_ktg_graph_data.sort_values(by='period_sort_index', inplace = True)

  # downtime_graph_data['downtime'] = downtime_graph_data['downtime'].astype(int)
  # ktg_graph_data['downtime'] = ktg_graph_data['downtime'].apply(lambda x: round(x, 0))
  
  downtime_ktg_graph_data.rename(columns={'period': 'Период', 'downtime': "Запланированный простой, час", "ktg": "КТГ"}, inplace=True)

  downtime_graph_data = downtime_ktg_graph_data.loc[:, ['Период', 'Запланированный простой, час']]

  x_month_year = downtime_graph_data['Период']
  y_downtime = downtime_graph_data['Запланированный простой, час']
  text_list_downtime_month_year = downtime_graph_data['Запланированный простой, час']
 
  if theme_selector:
      graph_template = 'seaborn'
  # bootstrap

  else:
      graph_template = 'plotly_dark'

  fig_downtime = go.Figure()
  fig_downtime.add_trace(go.Bar(
    name="Простои",
    x=x_month_year, 
    y=y_downtime,
    # xperiod="M1",
    # xperiodalignment="middle",
    #textposition='auto'
    ))
  # new_year_2022_2023 = pd.to_datetime('01.01.2024', format='%d.%m.%Y')
  # new_year_2023_2024 = pd.to_datetime('01.01.2025', format='%d.%m.%Y')
  # fig_downtime.add_vline(x=new_year_2022_2023, line_width=3, line_color="green")
  # fig_downtime.add_vline(x=new_year_2023_2024, line_width=3, line_color="green")

  fig_downtime.update_xaxes(
    showgrid=False, 
    # ticklabelmode="period"
  )
  fig_downtime.update_traces(
    text = text_list_downtime_month_year,
    textposition='auto'
  )
  fig_downtime.update_layout(
    title_text='Запланированный простой по месяцам за 3 года, час',
    template=graph_template,
    )
  
  ########################### ГРАФИК КТГ ###############################
  ktg_graph_data = downtime_ktg_graph_data.loc[:, ['Период', 'КТГ']]
  x_month_year_ktg = ktg_graph_data['Период']
  y_ktg = ktg_graph_data['КТГ']
  text_list_ktg_month_year = ktg_graph_data['КТГ']
  fig_ktg = go.Figure()
  fig_ktg.add_trace(go.Bar(
    name="КТГ",
    x=x_month_year_ktg, 
    y=y_ktg,
    # xperiod="M1",
    # xperiodalignment="middle",
    #textposition='auto'
    ))
  # new_year_2022_2023 = pd.to_datetime('01.01.2024', format='%d.%m.%Y')
  # new_year_2023_2024 = pd.to_datetime('01.01.2025', format='%d.%m.%Y')
  # fig_downtime.add_vline(x=new_year_2022_2023, line_width=3, line_color="green")
  # fig_downtime.add_vline(x=new_year_2023_2024, line_width=3, line_color="green")

  fig_ktg.update_xaxes(
    showgrid=False, 
    # ticklabelmode="period"
  )
  fig_ktg.update_traces(
    text = text_list_ktg_month_year,
    textposition='auto'
  )
  fig_ktg.update_layout(
    title_text='Запланированный КТГ по месяцам за 3 года',
    template=graph_template,
    )

  ############################ ТАБЛИЦА КТГ ##############################

  eo_model_list = list(set(downtime_ktg_graph_data['eo_model_name']))
  columns_list = initial_values.months_list
  columns_list = ['Модель ЕО'] + columns_list
  index_list = eo_model_list
  ktg_table_df = pd.DataFrame(columns=columns_list, index=index_list)
  # Сначала внешним циклом итерируемся по строкам таблицы - то есть по списку моделей ео
  for eo_model in eo_model_list:
    temp_dict = {}
    # делаем срез  - все записи текущей модели ео
    ktg_graph_data_selected = downtime_ktg_graph_data.loc[downtime_ktg_graph_data['eo_model_name'] == eo_model]
    
    temp_dict['Модель ЕО'] = eo_model
    # итерируемся по полученном временном срезу по модели
    for row in ktg_graph_data_selected.itertuples():
      month_year = getattr(row, 'month_year')
      ktg = getattr(row, 'КТГ')
      temp_dict[month_year] = ktg
    ktg_table_df.loc[eo_model] = pd.Series(temp_dict)
    
  ktg_table_df = ktg_table_df.rename(columns = initial_values.period_dict)
  ktg_table_df.index.name = 'Наименование модели ЕО'
  ktg_table_df.fillna(0, inplace = True)
  # ktg_table_df['Наименование модели'] = ktg_table_df.index
  ktg_table_df.to_csv('widget_data/ktg_table_data.csv', index = False)

  ############## РАСЧЕТ ГОДОВОГО КТГ #################################
  ktg_year_data = ktg_by_month_data_filtered.groupby(['year'], as_index=False)[['calendar_fond','downtime']].sum()

  ktg_year_data['ktg'] = (ktg_year_data['calendar_fond'] - ktg_year_data['downtime']) / ktg_year_data['calendar_fond']
  ktg_year_data['ktg'] = ktg_year_data['ktg'].apply(lambda x: round(x, 2))

  ktg_2023 = ktg_year_data.loc[ktg_year_data['year']==2023].iloc[0]['ktg']
  ktg_2024 = ktg_year_data.loc[ktg_year_data['year']==2024].iloc[0]['ktg']
  ktg_2025 = ktg_year_data.loc[ktg_year_data['year']==2025].iloc[0]['ktg']

  ############## РАЗВЕРТКА Р11 ###############################
  ktg_by_month_data_df_columns = ktg_by_month_data_filtered.columns
  job_list = list(pd.read_csv('data/job_list.csv')['maintanance_category_id'])
  actual_job_list = list(set(ktg_by_month_data_df_columns).intersection(job_list))
  
  actual_job_list_df = pd.DataFrame(actual_job_list, columns = ['maintanance_category_sort_index'])
  
  job_codes_df = pd.read_csv('data/job_codes.csv')
  
  
 
  column_list_groupping = ['downtime'] + actual_job_list

  # группируем в eo_main_class_description
  p11_raw_data = ktg_by_month_data_filtered.groupby(['eo_main_class_description', 'eo_model_name', 'year', 'month'], as_index = False)[column_list_groupping].sum()
  p11_raw_data['downtime'] = p11_raw_data['downtime'].apply(lambda x: round(x, 1))

  p11_raw_data.rename(columns=initial_values.rename_columns_dict, inplace=True)
  # print(p11_raw_data)

  # column_list = ['eo_main_class_description', 'eo_model_name', 'eo_description', 'eo_code', 'eo_description', 'operation_start_date', 'operation_finish_date', 'year', 'month'] + actual_job_list
  
  
  # p11_data = ktg_by_month_data_filtered.loc[:, column_list]
  
  p11data_transposed = p11_raw_data.transpose()
  p11data_transposed.reset_index(inplace = True)
  # print(p11data_transposed.index)
  # p11data_transposed.columns = p11data_transposed.iloc[0]
  # p11data_transposed_new = p11data_transposed[1:]
  # print(p11data_transposed_new.index)
  # p11data_transposed_new.reset_index(inplace = True)
  # print(p11data_transposed_new.index)
  #print(p11_raw_data)
  #p11_raw_data.reset_index()
  #print(p11_raw_data)
  p11data_transposed.to_csv('widget_data/p11data.csv', index = False)
  # p11data_transposed_new.to_csv('widget_data/p11data.csv')

  # p11data_transposed_new.loc[:, ['titles']] = p11data_transposed_new.index
  
  # print(list(p11data_transposed_new.index))
  # data=p11data_transposed_new.to_dict('records')
  # print(data)
  # p11data_transposed_new['titles'] = p11data_transposed_new.index
  # print(p11data_transposed_new.index)
  
  return fig_downtime, fig_ktg, ktg_table_df, ktg_2023, ktg_2024, ktg_2025, p11data_transposed
  


  
  

# widgets_data(True, ['first11'])
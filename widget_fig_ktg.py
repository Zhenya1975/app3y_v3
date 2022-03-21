import pandas as pd
import plotly.graph_objects as go
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

import functions
import initial_values

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
 
################# График КТГ по месяцам за три года ###############################
def fig_ktg_by_years(theme_selector, be_list_for_dataframes_filtering):
    
  '''График ктг по месяцам за три года'''
  
  # ktg_graph_data_df = pd.read_csv('widget_data/ktg_graph_data.csv')
  ktg_graph_data_df = functions.ktg_data_reading()
  ktg_graph_data_df = ktg_graph_data_df.loc[ktg_graph_data_df['level_1'].isin(be_list_for_dataframes_filtering)]
  # группируем
  
  ktg_graph_data = ktg_graph_data_df.groupby(['month_year'], as_index=False)[['calendar_fond', 'downtime']].sum()
  period_dict = initial_values.period_dict
    
  period_sort_index = initial_values.period_sort_index
  
  ktg_graph_data['period'] = ktg_graph_data['month_year'].map(period_dict).astype(str)
  
  ktg_graph_data['period_sort_index'] = ktg_graph_data['month_year'].map(period_sort_index)
  ktg_graph_data.sort_values(by='period_sort_index', inplace = True)
  # ktg_graph_data['downtime'] = ktg_graph_data['downtime'].astype(int)
  ktg_graph_data['ktg'] = (ktg_graph_data['calendar_fond'] - ktg_graph_data['downtime']) / ktg_graph_data['calendar_fond']
  ktg_graph_data['ktg'] = ktg_graph_data['ktg'].apply(lambda x: round(x, 2))
  
  ktg_graph_data.rename(columns={'period': 'Период', 'ktg': "КТГ"}, inplace=True)

  ktg_graph_data = ktg_graph_data.loc[:, ['Период', 'КТГ']]
  # ktg_graph_data.to_csv('data/ktg_graph_data_delete.csv')
  
  x_month_year = ktg_graph_data['Период']
  y_ktg = ktg_graph_data['КТГ']
  text_list_downtime_month_year = ktg_graph_data['КТГ']
 
  if theme_selector:
      graph_template = 'seaborn'
  # bootstrap

  else:
      graph_template = 'plotly_dark'

  fig_ktg = go.Figure()
  fig_ktg.add_trace(go.Bar(
    name="КТГ",
    x=x_month_year, 
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
  fig_ktg.update_yaxes(range = [0.5,1])
  
  fig_ktg.update_traces(
    text = text_list_downtime_month_year,
    textposition='auto'
  )
  fig_ktg.update_layout(
    title_text='Запланированный КТГ по месяцам за 3 года, час',
    template=graph_template,
    )

  return fig_ktg
  
  




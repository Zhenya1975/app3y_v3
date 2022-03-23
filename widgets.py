import pandas as pd
import plotly.graph_objects as go
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
import func_graph_downtime_data_prep
import initial_values
import functions

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
  ktg_by_month_data_filtered['month_year'] = ktg_by_month_data_filtered['month'].astype(str) + "_" + ktg_by_month_data_filtered['year'].astype(str)
  
  downtime_graph_data = ktg_by_month_data_filtered.groupby(['month_year'], as_index=False)['downtime'].sum()
  
  period_dict = initial_values.period_dict
    
  period_sort_index = initial_values.period_sort_index
  
  downtime_graph_data['period'] = downtime_graph_data['month_year'].map(period_dict).astype(str)
  
  downtime_graph_data['period_sort_index'] = downtime_graph_data['month_year'].map(period_sort_index)
  downtime_graph_data.sort_values(by='period_sort_index', inplace = True)
  
  # downtime_graph_data['downtime'] = downtime_graph_data['downtime'].astype(int)
  # ktg_graph_data['downtime'] = ktg_graph_data['downtime'].apply(lambda x: round(x, 0))
  
  downtime_graph_data.rename(columns={'period': 'Период', 'downtime': "Запланированный простой, час"}, inplace=True)
  downtime_graph_data = downtime_graph_data.loc[:, ['Период', 'Запланированный простой, час']]

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

  return fig_downtime

  
  

# widgets_data(['first11'])
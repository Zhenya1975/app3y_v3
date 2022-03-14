import pandas as pd
import plotly.graph_objects as go
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

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
def fig_ktg_by_years(theme_selector):
    
  '''График ктг по месяцам за три года'''
  ktg_graph_data_df = pd.read_csv('widget_data/ktg_graph_data.csv')
  x_month_year = ktg_graph_data_df['Период']
  y_ktg = ktg_graph_data_df['Запланированный КТГ']
  text_list_downtime_month_year = ktg_graph_data_df['Запланированный КТГ']
 
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
  
  




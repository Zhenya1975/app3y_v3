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

def fig_downtime_by_years_data(maintanance_jobs_df):
  maintanance_jobs_df = maintanance_jobs_df.loc[:, ["dowtime_plan, hours", "month_year", "month_year_sort_index"]]
  # print(maintanance_jobs_df.info())
  maintanance_jobs_df_groupped = maintanance_jobs_df.groupby(["month_year", "month_year_sort_index"], as_index=False)["dowtime_plan, hours"].sum()
  # print(maintanance_jobs_df_groupped)
  # x_month_year = ['1_2023','2_2023','3_2023','4_2023','5_2023','6_2023','7_2023','8_2023','9_2023','10_2023','11_2023','12_2023','1_2024','2_2024','3_2024','4_2024','5_2024','6_2024','7_2024','8_2024','9_2024','10_2024','11_2024','12_2024','1_2025','2_2025','3_2025','4_2025','5_2025','6_2025','7_2025','8_2025','9_2025','10_2025','11_2025','12_2025']
  x_month_year = maintanance_jobs_df_groupped['month_year']
  y_downtime = maintanance_jobs_df_groupped['dowtime_plan, hours']
  text_list_downtime_month_year = maintanance_jobs_df_groupped['dowtime_plan, hours']
  maintanance_jobs_df_groupped.sort_values(by=['month_year_sort_index'],inplace = True)
  maintanance_jobs_df_groupped.to_csv("widget_data/fig_downtime_by_years_data.csv", index = False)

 

################# График простоев по месяцам за три года ###############################
def fig_downtime_by_years(maintanance_jobs_df, theme_selector):
    
  '''График простоев по месяцам за три года'''
  fig_downtime_data = pd.read_csv("widget_data/fig_downtime_by_years_data.csv")
  x_month_year =fig_downtime_data['month_year']
  y_downtime = fig_downtime_data['dowtime_plan, hours']
  text_list_downtime_month_year = fig_downtime_data['dowtime_plan, hours']
  #downtime_y = maintanance_jobs_df['dowtime_plan, hours']
  #dates_x = maintanance_jobs_df['maintanance_datetime']
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
  
  




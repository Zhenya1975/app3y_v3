import pandas as pd
# import numpy as np
from dash import Dash, dcc, html, Input, Output, callback_context, State, callback_context
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import datetime

import tab_main
import functions
import widget_fig_downtime
import widget_fig_ktg
import widget_fig_piechart_downtime_2023
import ktg_table_html
# import tab_coverage
# import tab_settings



# import functions
# import title_text
# import fig_downtime_by_years
# import table_maintanance_xlsx
# import fig_ktg_by_years
# import fig_planned_3y_ktg
# import fig_piechart_downtime_by_categories
# import ktg_by_month_models
# import ktg_table_html



# import initial_values

from dash import dash_table
import base64
import io
import json
import plotly.graph_objects as go
# import fig_coverage

# select the Bootstrap stylesheet2 and figure template2 for the theme toggle here:
# template_theme1 = "sketchy"
template_theme1 = "flatly"
template_theme2 = "darkly"
# url_theme1 = dbc.themes.SKETCHY
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY



loading_style = {
    # 'position': 'absolute',
                 # 'align-self': 'center'
                 }

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
app = Dash(__name__, external_stylesheets=[url_theme1, dbc_css])

"""
===============================================================================
Layout
"""

tabs_styles = {
    'height': '34px'
}



app.layout = dbc.Container(
    dbc.Row(        [
            dbc.Col(
                [
                    html.H4("КТГ 2023-2025"),
                    ThemeSwitchAIO(
                      aio_id="theme", themes=[url_theme1, url_theme2],
                    ),

                    html.Div([
                        dcc.Tabs(
                            id="tabs-all",
                            style={
                                # 'width': '50%',
                                # 'font-size': '200%',
                                'height':'10vh'
                            },
                            value='ktg',
                            # parent_className='custom-tabs',
                            # className='custom-tabs-container',
                            children=[
                                tab_main.maintanance_chart_tab(),
                                # coverage_tab.coverage_tab(),
                                # messages_orders_tab.messages_orders_tab(),
                                # orders_moved_tab.orders_moved_tab(),
                                # settings_tab.settings_tab()

                                # tab2(),
                                # tab3(),
                            ]
                        ),
                    ]),

                ]
            )
        ]
    ),
    className="m-4 dbc",
    fluid=True,
    
)


######################### ОСНОВНОЙ ОБРАБОТЧИК ДЛЯ ПОСТРОЕНИЯ ГРАФИКОВ ##############################
@app.callback([
    Output('eo_qty_2023', 'children'),
    Output('eo_qty_2024', 'children'),
    Output('eo_qty_2025', 'children'),
    Output('planned_downtime', 'figure'),
    Output('fig_ktg_3y_by_months_id', 'figure'),
    Output('planned_downtime_piechart_2023', 'figure'),

    Output('ktg_by_month_table', 'children'),
    Output('loading', 'parent_style'),

],
    [
      Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
      Input("btn_update", "n_clicks"),

    ],
)

def maintanance(theme_selector, btn_update_n_click):
  
  changed_id = [p['prop_id'] for p in callback_context.triggered][0]
  if theme_selector:
      graph_template = 'sandstone'
  # bootstrap

  else:
      graph_template = 'plotly_dark'

  maintanance_jobs_df = functions.maintanance_jobs_df()
  # при нажатии на кнопку обновляем csv для построения графиков
  if btn_update_n_click:
    # Обновление данных для построения графика
    functions.pass_interval_fill()
    functions.maintanance_category_prep()
    functions.eo_job_catologue()
    functions.maintanance_jobs_df_prepare()
    functions.fill_calendar_fond()
    functions.hour_calculation()
    functions.eo_list_download_preparation()
    functions.maint_jobs_download_preparation()
    functions.downtime_by_categiries_2023_data()

  fig_downtime = widget_fig_downtime.fig_downtime_by_years(theme_selector)

  fig_ktg = widget_fig_ktg.fig_ktg_by_years(theme_selector)

  fig_piechart_downtime_2023 = widget_fig_piechart_downtime_2023.fig_piechart_downtime_2023(theme_selector)
  
  total_qty_EO_2023 = functions.total_qty_EO()[0]
  total_qty_EO_2024 = functions.total_qty_EO()[1]
  total_qty_EO_2025 = functions.total_qty_EO()[2]
  
  eo_qty_2023_card_text = 'Кол-во ЕО в выборке: {}'.format(total_qty_EO_2023)
  eo_qty_2024_card_text = 'Кол-во ЕО в выборке: {}'.format(total_qty_EO_2024)
  eo_qty_2025_card_text = 'Кол-во ЕО в выборке: {}'.format(total_qty_EO_2025)
  
  df_ktg_table = pd.read_csv('data/model_hours_ktg_data.csv')
  ktg_by_month_table = ktg_table_html.ktg_table(df_ktg_table)

  new_loading_style = loading_style
  return eo_qty_2023_card_text,eo_qty_2024_card_text, eo_qty_2025_card_text, fig_downtime, fig_ktg, fig_piechart_downtime_2023, ktg_by_month_table, new_loading_style










  
####################### ОБРАБОТЧИК ВЫГРУЗКИ ЕО В EXCEL #####################################
@app.callback(
    Output("download_excel_eo_table", "data"),
    Input("btn_download_eo_table", "n_clicks"),
    prevent_initial_call=True,)
def funct(n_clicks_eo_table):
  # df = pd.read_csv('widget_data/eo_download_data.csv', dtype = str)
  df = pd.read_csv('widget_data/eo_download_data.csv', dtype = str, decimal=",")
  # df['Среднесуточная наработка'].apply(lambda x: x.replace(',','.'))
  # df['Среднесуточная наработка'] = df['Среднесуточная наработка'].astype(float)
  if n_clicks_eo_table:
    return dcc.send_data_frame(df.to_excel, "EO в выборке КТГ.xlsx", index=False, sheet_name="EO в выборке КТГ")


####################### ОБРАБОТЧИК ВЫГРУЗКИ РАБОТ В EXCEL #####################################
@app.callback(
    Output("download_excel_maint_jobs_table", "data"),
    Input("btn_download_maint_jobs_table", "n_clicks"),
    prevent_initial_call=True,)
def funct_maint_jobs_table(n_clicks_maint_jobs_table):
  # df = pd.read_csv('widget_data/eo_download_data.csv', dtype = str)
  df = pd.read_csv('widget_data/maint_jobs_download_data.csv', dtype = str, decimal=",")

  if n_clicks_maint_jobs_table:
    return dcc.send_data_frame(df.to_excel, "ТОИР воздействия.xlsx", index=False, sheet_name="ТОИР воздействия")


if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(host='0.0.0.0', debug=True)
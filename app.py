import pandas as pd
# import numpy as np
from dash import Dash, dcc, html, Input, Output, callback_context, State, callback_context
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import datetime

import tab_main
import settings_tab
import functions
import func_maintanance_jobs_df_prepare
import func_ktg_data_prep
import widget_fig_downtime
import widget_fig_ktg
import widget_fig_piechart_downtime_2023
import widget_fig_piechart_downtime_2024
import widget_fig_piechart_downtime_2025
import ktg_table_html
import func_be_select_data_prep
import func_graph_downtime_data_prep
import widget_table_ktg
import widget_download_eo
import widget_download_maint_jobs
import widgets

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
                                settings_tab.settings_tab()

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
    Output("checklist_level_1", "value"),
    Output("checklist_level_1", "options"),
    Output('eo_qty_2023', 'children'),
    Output('eo_qty_2024', 'children'),
    Output('eo_qty_2025', 'children'),
    Output('planned_downtime', 'figure'),
    Output('fig_ktg_3y_by_months_id', 'figure'),
    

    Output('ktg_by_month_table', 'children'),
    Output('loading', 'parent_style'),

],
    [
      Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
      Input('checklist_level_1', "value"),

      # Input("btn_update", "n_clicks"),

    ],
)

# def maintanance(theme_selector, btn_update_n_click):
def maintanance(theme_selector, checklist_be):  
   # читаем файл с дефолтными фильтрами
    # Opening JSON file
  with open('saved_filters.json', 'r') as openfile:
    # Reading from json file
    saved_filters_dict = json.load(openfile)

  
  changed_id = [p['prop_id'] for p in callback_context.triggered][0]
  if theme_selector:
      graph_template = 'sandstone'
  # bootstrap

  else:
      graph_template = 'plotly_dark'
  # if checklist_be == None:
  #   be_filter = func_be_select_data_prep.be_select_data_prep()[1]
  # elif checklist_be != None:
  #   be_filter = checklist_be
    
  # maintanance_jobs_df = functions.maintanance_jobs_df()
  
  # при нажатии на кнопку обновляем csv для построения графиков
  # if btn_update_n_click:
  #   # Обновление данных для построения графика
  #   functions.pass_interval_fill()
  #   functions.maintanance_category_prep()
  #   functions.eo_job_catologue()
  #   func_maintanance_jobs_df_prepare.maintanance_jobs_df_prepare()
  #   functions.fill_calendar_fond()
  #   functions.hour_calculation()
  #   functions.eo_list_download_preparation()
  #   functions.maint_jobs_download_preparation()
  #   functions.downtime_by_categiries_data()
  #   functions.ktg_graph_data_preparation()
  #   functions.ktg_table_prep()
  
  

  # если фильтр не трогали и его значение равно None, то вытаскиваем значение из сохраненного фильтра
  be_full_list = func_be_select_data_prep.be_select_data_prep()[2]
  
  if checklist_be == None:
    checklist_be_value = saved_filters_dict['filter_be']
    if len(checklist_be_value) == 0:
      be_list_for_dataframes_filtering = be_full_list
    else:
      be_list_for_dataframes_filtering = checklist_be_value

  # если в фильтре что-то есть и он не пустой то берем значение из фильтра и переписываем json
  elif checklist_be != None and len(checklist_be) != 0:
    be_list_for_dataframes_filtering = checklist_be
    saved_filters_dict['filter_be'] = checklist_be
    # записываем в json
    with open("saved_filters.json", "w") as jsonFile:
      json.dump(saved_filters_dict, jsonFile)
    checklist_be_value = checklist_be
  # ессли фильтр трогали, но очистили то фильтр надо очистить
  elif len(checklist_be) == 0:
    be_list_for_dataframes_filtering = be_full_list
    saved_filters_dict['filter_be'] = checklist_be
    # записываем в json
    with open("saved_filters.json", "w") as jsonFile:
      json.dump(saved_filters_dict, jsonFile)
    checklist_be_value = checklist_be
  # checklist_be_value = []
  checklist_be_options = func_be_select_data_prep.be_select_data_prep()[0]

  # таким образом, мы получили значение из фильтра be и теперь можем отфильтровать данные для виджетов
  
  # fig_downtime_data = func_graph_downtime_data_prep.graph_downtime_data_prep(be_list_for_dataframes_filtering)
  # fig_downtime = widget_fig_downtime.fig_downtime_by_years(theme_selector, fig_downtime_data)
  fig_downtime = widgets.widgets_data(theme_selector, be_list_for_dataframes_filtering)

  total_qty_EO_2023 = functions.total_qty_EO(be_list_for_dataframes_filtering)[0]
  total_qty_EO_2024 = functions.total_qty_EO(be_list_for_dataframes_filtering)[1]
  total_qty_EO_2025 = functions.total_qty_EO(be_list_for_dataframes_filtering)[2]
  
  eo_qty_2023_card_text = 'Кол-во ЕО в выборке: {}'.format(total_qty_EO_2023)
  eo_qty_2024_card_text = 'Кол-во ЕО в выборке: {}'.format(total_qty_EO_2024)
  eo_qty_2025_card_text = 'Кол-во ЕО в выборке: {}'.format(total_qty_EO_2025)

  fig_ktg = widget_fig_ktg.fig_ktg_by_years(theme_selector, be_list_for_dataframes_filtering)

  # df_ktg_table = pd.read_csv('widget_data/ktg_table_data.csv')
  df_ktg_table = widget_table_ktg.ktg_table_prep(be_list_for_dataframes_filtering)
  ktg_by_month_table = ktg_table_html.ktg_table(df_ktg_table)

  # обновить csv для выгрузки eo
  widget_download_eo.eo_list_download_preparation(be_list_for_dataframes_filtering)
  # обновить csv для выгрузки данных о работах
  widget_download_maint_jobs.maint_jobs_download_preparation(be_list_for_dataframes_filtering)

  
  new_loading_style = loading_style
  return checklist_be_value, checklist_be_options, eo_qty_2023_card_text,eo_qty_2024_card_text, eo_qty_2025_card_text, fig_downtime, fig_ktg, ktg_by_month_table, new_loading_style










  
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

####################### ОБРАБОТЧИК ВЫГРУЗКИ КТГ В EXCEL #####################################
@app.callback(
    Output("download_excel_ktg_table", "data"),
    Input("btn_download_ktg_table", "n_clicks"),
    prevent_initial_call=True,)
def funct_ktg_table(n_clicks_ktg_table):
  # df = pd.read_csv('widget_data/eo_download_data.csv', dtype = str)
  df = pd.read_csv('widget_data/ktg_table_data.csv', dtype = str, decimal=",")

  if n_clicks_ktg_table:
    return dcc.send_data_frame(df.to_excel, "КТГ по месяцам.xlsx", index=False, sheet_name="КТГ по месяцам")



########## Настройки################

# Обработчик кнопки выгрузки в эксель таблицы с регламентом ТОИР
@app.callback(
    Output("download_maintanance_job_list_general", "data"),
    Input("btn_download_maintanance_job_list_general", "n_clicks"),
    prevent_initial_call=True,)
def funct(n_clicks_ktg_table):
  df = pd.read_csv('data/maintanance_job_list_general.csv')
  if n_clicks_ktg_table:
    return dcc.send_data_frame(df.to_excel, "maintanance_job_list.xlsx", index=False, sheet_name="maintanance_job_list")

# Обработчик кнопки расчета maintanance_jobs_df
@app.callback(
    Output("output-data-2", "children"),
    Input("btn_calc_maintanance_jobs_df", "n_clicks"),
    )
def funct_maintanance_job_list_general_calc(n_clicks_maintanance_jobs_df_calc):
  message_result = ""
  if n_clicks_maintanance_jobs_df_calc:
    func_maintanance_jobs_df_prepare.maintanance_jobs_df_prepare()
    # читаем результат
    maintanance_jobs_df = functions.maintanance_jobs_df()
    # список моделей
    model_list = list(set(maintanance_jobs_df['eo_model_name']))
    message_dict = {}
    for model in model_list:
      #режем выборку по модели
      maintanance_jobs_df_selected = maintanance_jobs_df.loc[maintanance_jobs_df['eo_model_name'] ==model]
      # определяем количество ео в выборке
      
      eo_qty = len(list(set(maintanance_jobs_df_selected['eo_code'])))
      message_dict[model] = eo_qty
    message_result = "maintanance_jobs_df_calc пересчитан. {} единицы".format(message_dict)  
  return message_result

# Обработчик кнопки расчета ktg_data_prep
@app.callback(
    Output("output-data-3", "children"),
    Input("btn_calc_ktg_data", "n_clicks"),
    )
def funct_ktg_data_prep_calc(n_clicks_ktg_data_prep_calc):
  message_result = ""
  if n_clicks_ktg_data_prep_calc:
    func_ktg_data_prep.ktg_data_prep()
    # читаем результат
    # maintanance_jobs_df = functions.maintanance_jobs_df()
    # # список моделей
    # model_list = list(set(maintanance_jobs_df['eo_model_name']))
    # message_dict = {}
    # for model in model_list:
    #   #режем выборку по модели
    #   maintanance_jobs_df_selected = maintanance_jobs_df.loc[maintanance_jobs_df['eo_model_name'] ==model]
    #   # определяем количество ео в выборке
      
    #   eo_qty = len(list(set(maintanance_jobs_df_selected['eo_code'])))
    #   message_dict[model] = eo_qty
    # message_result = "maintanance_jobs_df_calc пересчитан. {} единицы".format(message_dict)  
    message_result = "ktg_data пересчитан" 
  return message_result




def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xlsx' in filename and "maintanance_job_list_general" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded),decimal=',')
            

            # проверяем, что в файле есть нужные колонки 
            list_of_columns_in_uploaded_df = df.columns.tolist()
            check_column_list = ['maintanance_code_id', 'maintanance_code', 'maintanance_category_id','upper_level_tehmesto_code', 'maintanance_name', 'interval_motohours', 'downtime_planned', 'pass_interval', 'source']
            control_value = 1
            
            for column in check_column_list:
              if column in list_of_columns_in_uploaded_df:
                continue
              else:
                control_value = 0
          
                break
     
            if control_value == 1:
       
              df.to_csv('data/maintanance_job_list_general.csv')
              print("maintanance_job_list_general загружен")
              functions.pass_interval_fill()
              functions.maintanance_category_prep()
              functions.eo_job_catologue()
              print("eo_job_catologue обновлен")
              
            else:
              print('не хватает колонок')
            
            # если мы загрузили список с работами, то надо подготовить данные для того чтобы вставить
            # даты начала расчета для ТО-шек
            

        elif 'xlsx' in filename and "eo_job_catologue" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            # values = {"last_maintanance_date": default_to_start_date.date()}

            #df.fillna(value=values)
  
            updated_eo_maintanance_job_code_last_date = df.loc[:, ['eo_maintanance_job_code', 'last_maintanance_date']]
            
            functions.fill_calendar_fond()
            #functions.maintanance_matrix()
            functions.eo_job_catologue()
            functions.maintanance_jobs_df_prepare()
        
            updated_eo_maintanance_job_code_last_date.to_csv('data/eo_maintanance_job_code_last_date.csv')

        # загружаем список eo - в ответ получаем список для перепроверки даты ввода в эксплуатацию, даты списания, среднесуточной наработки
        elif 'xlsx' in filename and "eo_request_data" in filename:
          # Assume that the user uploaded an excel file
          df_eo_request_list = pd.read_excel(io.BytesIO(decoded), dtype=str)
          # объединяем с full_eo_list
          eo_list = pd.read_csv('data/full_eo_list_actual.csv', dtype=str)
          eo_list_data = pd.merge(df_eo_request_list, eo_list, on = 'eo_code', how = 'left')
          # объединяем с level_1
          level_1 = pd.read_csv('data/level_1.csv')
          eo_list_data = pd.merge(eo_list_data, level_1, on = 'level_1', how = 'left')
          # объединяем с level_upper
          level_upper = pd.read_csv('data/level_upper.csv', dtype=str)
          eo_list_data = pd.merge(eo_list_data, level_upper, on = 'level_upper', how = 'left')
          # объединяем с level_2
          level_2 = pd.read_csv('data/level_2_list.csv', dtype=str)
          eo_list_data = pd.merge(eo_list_data, level_2, on = 'level_2_path', how = 'left')
          date_columns = ["operation_start_date", "operation_finish_date"]
          # Колонку со строкой - в дату
          for column in date_columns:
            eo_list_data[column] =  eo_list_data[column].astype("datetime64[ns]")
            # колонку  с datetime - в строку
            eo_list_data[column] = eo_list_data[column].dt.strftime("%d.%m.%Y")
          
          eo_list_data = eo_list_data.loc[:, ['level_1_description', 'Название технического места', 'eo_code', 'eo_description', 'mvz', 'level_2_description', 'operation_start_date','operation_finish_date', 'avearage_day_operation_hours']]
          eo_list_data.to_csv('data/eo_list_data_temp.csv', index = False)
          
          # print(df_eo_request_list)
          df = df_eo_request_list
          
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),


        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            filter_action='native',
            style_header={
                # 'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_cell={'textAlign': 'left'},

        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              )
def update_output_(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)]
        
        return children




if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(host='0.0.0.0', debug=True)
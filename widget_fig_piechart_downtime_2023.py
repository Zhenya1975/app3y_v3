import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
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
available_graph_templates: ['ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark',
                            'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none']
load_figure_template(templates)

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"
)


############# PIECHART ПРОСТОИ ПО КАТЕГОРИЯМ #####################
def fig_piechart_downtime_2023(theme_selector, be_list_for_dataframes_filtering):
    # downtime_by_categiries_2023 = pd.read_csv('widget_data/downtime_by_categiries_2023_data.csv')
    ktg_by_month_data_df = functions.ktg_data_reading()
    ktg_by_month_data_df = ktg_by_month_data_df.loc[ktg_by_month_data_df['level_1'].isin(be_list_for_dataframes_filtering)]
   
    ktg_by_month_data_df['downtime'] = ktg_by_month_data_df['downtime'].astype(float)
    job_list_df = pd.read_csv('data/job_list.csv')
    job_list = list(job_list_df['maintanance_category_id'])
    columns_list = job_list + ['downtime']
    ktg_by_month_data_df_2023 = ktg_by_month_data_df.loc[ktg_by_month_data_df['year'] == 2023]
    downtime_by_categories_2023 = ktg_by_month_data_df_2023.groupby(['year'], as_index=False)[columns_list].sum()
    total_downtime = downtime_by_categories_2023.iloc[0]['downtime']


    labels = []
    values = []

    for job_code in job_list:
        downtime_value = downtime_by_categories_2023.iloc[0][job_code]
        if total_downtime !=0:
          downtime_value_dolya = downtime_value / total_downtime
        else:
          downtime_value_dolya = 0
        if downtime_value_dolya >0.02:
            labels.append(job_code)
            values.append(downtime_value)
    # print(labels)
    # print(values)




    # labels = list(downtime_by_categories_2023['Вид ТОРО'])
    # values = list(downtime_by_categories_2023['Простой, час'])
    if theme_selector:
        graph_template = 'seaborn'
    else:
        graph_template = 'plotly_dark'

    planned_downtime_2023_piechart = go.Figure(data=[go.Pie(labels=labels, values=values)])
    # planned_downtime_piechart.update_traces(textposition='inside')
    planned_downtime_2023_piechart.update_layout(
        # margin=dict(t=0, b=0, l=0, r=0),
        autosize=False,
        width=500,
        height=500,
        title_text='Простой по видам работ, 2023',
        template=graph_template,
        # uniformtext_minsize=12, uniformtext_mode='hide',
        legend=dict(
            # font=dict(color='#7f7f7f'),
            # orientation="h", # Looks much better horizontal than vertical
            # y=0.6,
            x=1.6
        ),
    )
    return planned_downtime_2023_piechart

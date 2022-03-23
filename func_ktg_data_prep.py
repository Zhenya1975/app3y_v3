import pandas as pd
from datetime import timedelta
import functions
import initial_values

import func_be_select_data_prep

last_day_of_selection = initial_values.last_day_of_selection

def hour_table_df():
  """Подготовка заготовки с часами по трем годам"""
  start_point = pd.to_datetime('01.01.2023', format='%d.%m.%Y')
  current_hour = start_point

  hour_df_data = []
  while current_hour < last_day_of_selection:
      temp_dict = {}
      temp_dict['model_hour'] = current_hour
      temp_dict["calendar_fond"] = 0
      temp_dict["downtime"] = 0
      hour_df_data.append(temp_dict)
      temp_dict['year'] = current_hour.year
      temp_dict['month'] = current_hour.month
      temp_dict['hour'] = current_hour.hour
      temp_dict['maintanance_name'] = []
      current_hour = current_hour + timedelta(hours=1)
  hour_df = pd.DataFrame(hour_df_data)
  return hour_df

def ktg_data_prep():
  """подготовка данных для расчета ктг"""
  # читаем maintanance_jobs_df
  maintanance_jobs_df = functions.maintanance_jobs_df()
  # читаем full_eo_list
  full_eo_list = functions.full_eo_list_func()
  # eo_list = ['100000084504', '100000084492']
  # eo_list = ['100000065619']

  eo_list = list(set(maintanance_jobs_df['eo_code']))
  # итерируемся по списку ео
  job_list = list(pd.read_csv('data/job_list.csv')['maintanance_category_id'])
  column_list = ['calendar_fond', 'downtime'] + job_list
  ktg_by_month_data_df = pd.DataFrame(columns=column_list)
  ktg_by_month_data_df = pd.DataFrame()

  hour_df = hour_table_df()
  i=1
  for eo in eo_list:
    progress_text = "eo " + str(i) + " из " + str(len(eo_list))

    print(progress_text)
    i = i+1
    # получаем заготовку hour_df
    hour_df = hour_table_df()
    # print("получили заготовку hour_df")


    # заполняем колонку calendar_fond единичками в диапазоне срока эксплуатации машины
    maintanance_start_datetime = full_eo_list.loc[full_eo_list['eo_code'] == eo, ['operation_start_date']].values[0][0]
    maintanance_finish_datetime = full_eo_list.loc[full_eo_list['eo_code'] == eo, ['operation_finish_date']].values[0][0]
    # print("получили даты начала и конца эксплуатации ео", eo)
    # режем таблицу hour_df между датами operation_start_date и operation_finish_date
    hour_df_operation = hour_df.loc[
            (hour_df['model_hour'] >= maintanance_start_datetime) &
            (hour_df['model_hour'] <= maintanance_finish_datetime)]
    # записываем единичку в поле calendar_fond
    indexes_operation_period = hour_df_operation.index.values
    hour_df.loc[indexes_operation_period, ['calendar_fond']] = 1
    # print("записали в hour_df единички в calendar_fond", eo)

    # режем таблицу maintanance_jobs_df по ео
    maintanance_jobs_df_selected_by_eo = maintanance_jobs_df.loc[maintanance_jobs_df["eo_code"] == eo]

    # сначала расставляем значение из eto
    
    eto_df = maintanance_jobs_df_selected_by_eo.loc[maintanance_jobs_df_selected_by_eo['maintanance_category_id'] == "eto"]
    eto_start_hour = eto_df.iloc[0]['hour']
    downtime_plan = eto_df.iloc[0]['downtime_plan']
    hour_df_filtered_by_eto_hour = hour_df.loc[hour_df['hour']==eto_start_hour]
    
    hour_df_filtered_by_eto_hour = hour_df_filtered_by_eto_hour.loc[
            (hour_df_filtered_by_eto_hour['model_hour'] >= maintanance_start_datetime) &
            (hour_df_filtered_by_eto_hour['model_hour'] <= maintanance_finish_datetime)]
    
    hour_df_filtered_by_eto_hour_indexes = hour_df_filtered_by_eto_hour.index.values
    
    hour_df.loc[hour_df_filtered_by_eto_hour_indexes, ['downtime', 'eto']] = downtime_plan

    
    # записываем единички в простои, не равные ето
    maint_df = maintanance_jobs_df_selected_by_eo.loc[maintanance_jobs_df_selected_by_eo['maintanance_category_id'] != "eto"]
    # print(maint_df)
    for row in maint_df.itertuples():
      maintanance_jobs_id = getattr(row, "maintanance_jobs_id")
      maintanance_name = getattr(row, "maintanance_name")
      maintanance_category_id = getattr(row, "maintanance_category_id")
      maintanance_start_datetime = getattr(row, "maintanance_start_datetime")
      maintanance_finish_datetime = getattr(row, "maintanance_finish_datetime")
      downtime_plan = getattr(row, "downtime_plan")

      # режем hours_df в диапазоне maintanance_start_datetime	maintanance_finish_datetime
      model_hours_df_cut_by_maint_job = hour_df.loc[
          (hour_df['model_hour'] >= maintanance_start_datetime) &
          (hour_df['model_hour'] <= maintanance_finish_datetime)]
      indexes_maint_job = model_hours_df_cut_by_maint_job.index.values

      # записываем единичку в поле downtime
      hour_df.loc[indexes_maint_job, ['downtime']] = 1
      hour_df.loc[indexes_maint_job, ['maintanance_name']] = hour_df.loc[indexes_maint_job, ['maintanance_name']] + [[maintanance_name]]
      hour_df.loc[indexes_maint_job, [maintanance_category_id]] = 1
      
      
    # заполняем пустые ячейки нулями
    hour_df.fillna(0, inplace=True)
    # hour_df.to_csv('data/hour_df_temp_delete.csv')  
    job_list = list(pd.read_csv('data/job_list.csv')['maintanance_category_id'])

    eo_calendar_fond_downtime_by_month = hour_df.groupby(['year', 'month'], as_index=False)[column_list].sum()
    
    
    eo_calendar_fond_downtime_by_month['eo_code'] = eo
    
    
    ktg_by_month_data_df = pd.concat([ktg_by_month_data_df, eo_calendar_fond_downtime_by_month], ignore_index=True)
    
    # print("завершен цикл по ", eo)

  ktg_by_month_data_df.fillna(0, inplace=True)
  # объединяем с таблицей машин
  # print("перед объединением с full eo list")
  eo_data = full_eo_list.loc[:, ['eo_code', 'level_1', 'eo_model_name', 'eo_description', 'teh_mesto', 'mvz', 'constr_type', 'avearage_day_operation_hours_updated', 'operation_start_date', 'avearage_day_operation_hours',	'operation_finish_date', 'eo_main_class_description']]
  ktg_by_month_data_df = pd.merge(ktg_by_month_data_df, eo_data, how='left', on='eo_code')
  # print("после объединения с full eo list")
  ktg_by_month_data_df.to_csv('widget_data/ktg_by_month_data_df.csv', decimal=",", index=False)
  # пересчитываем csv графика простоев
  # print("перед пересчетом графиика простоев")
  # func_graph_downtime_data_prep.graph_downtime_data_prep()
  # пересчитываем данные для списка фильтра БЕ
  # func_be_select_data_prep.be_select_data_prep()


  



# ktg_data_prep()


import pandas as pd
from datetime import timedelta
import functions
import initial_values

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
    eo_list = ['100000084504', '100000084492']
    # получаем заготовку hour_df
    hour_df = hour_table_df()
    # итерируемся по списку ео
    ktg_by_month_data_df = pd.DataFrame(columns=['eo_code', 'year', 'month', 'calendar_fond', 'downtime'])

    for eo in eo_list:
        # заполняем колонку calendar_fond единичками в диапазоне срока эксплуатации машины
        maintanance_start_datetime = full_eo_list.loc[full_eo_list['eo_code'] == eo, ['operation_start_date']].values[0][0]
        maintanance_finish_datetime = full_eo_list.loc[full_eo_list['eo_code'] == eo, ['operation_finish_date']].values[0][0]

        # режем таблицу hour_df между датами operation_start_date и operation_finish_date
        hour_df_operation = hour_df.loc[
                (hour_df['model_hour'] >= maintanance_start_datetime) &
                (hour_df['model_hour'] <= maintanance_finish_datetime)]
        # записываем единичку в поле calendar_fond
        indexes_operation_period = hour_df_operation.index.values
        hour_df.loc[indexes_operation_period, ['calendar_fond']] = 1


        # режем таблицу maintanance_jobs_df по ео
        maintanance_jobs_df_selected_by_eo = maintanance_jobs_df.loc[maintanance_jobs_df["eo_code"] == eo]

        # итерируемся по maintanance_jobs_df_selected_by_eo
        # сначала расставляем значение из eto
        eto_df = maintanance_jobs_df_selected_by_eo.loc[maintanance_jobs_df_selected_by_eo['maintanance_category_id'] == "eto"]
        for row in eto_df.itertuples():
            maintanance_jobs_id = getattr(row, "maintanance_jobs_id")
            maintanance_category_id = getattr(row, "maintanance_category_id")
            maintanance_start_datetime = getattr(row, "maintanance_start_datetime")
            maintanance_finish_datetime = getattr(row, "maintanance_finish_datetime")
            downtime_plan = getattr(row, "downtime_plan")

            # режем hours_df в диапазоне maintanance_start_datetime	maintanance_finish_datetime
            model_hours_df_cut_by_maint_job = hour_df.loc[
                (hour_df['model_hour'] >= maintanance_start_datetime) &
                (hour_df['model_hour'] <= maintanance_finish_datetime)]
            indexes_maint_job = model_hours_df_cut_by_maint_job.index.values

            # записываем значение простоя на ето в поле downtime
            hour_df.loc[indexes_maint_job, ['downtime']] = downtime_plan
            hour_df.loc[indexes_maint_job, ['maintanance_name']] = hour_df.loc[indexes_maint_job, ['maintanance_name']] + [['eto']]

        # вторым проходом записываем единички в простои, не равные ето
        maint_df = maintanance_jobs_df_selected_by_eo.loc[maintanance_jobs_df_selected_by_eo['maintanance_category_id'] != "eto"]
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


        # Теперь собираем результат в месяцы
        eo_calendar_fond_downtime_by_month = hour_df.groupby(['year', 'month'], as_index=False)[['calendar_fond', 'downtime']].sum()
        eo_calendar_fond_downtime_by_month['eo_code'] = eo
        ktg_by_month_data_df = pd.concat([ktg_by_month_data_df, eo_calendar_fond_downtime_by_month], ignore_index=True)

    # объединяем с таблицей машин
    eo_data = full_eo_list.loc[:, ['eo_code', 'level_1_description', 'eo_model_name', 'eo_description', 'teh_mesto', 'mvz', 'constr_type', 'avearage_day_operation_hours_updated', 'operation_start_date', 'avearage_day_operation_hours',	'operation_finish_date', 'eo_main_class_description']]
    ktg_by_month_data_df = pd.merge(ktg_by_month_data_df, eo_data, how='left', on='eo_code')
    ktg_by_month_data_df.to_csv('data/ktg_by_month_data_df.csv', decimal=",", index=False)
    hour_df.to_csv('data/hour_df.csv', decimal=",")





ktg_data_prep()



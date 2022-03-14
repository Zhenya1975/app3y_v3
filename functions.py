import pandas as pd
import initial_values
from datetime import timedelta

first_day_of_selection = initial_values.first_day_of_selection
last_day_of_selection = initial_values.last_day_of_selection


# print(timedelta(hours=50.0))

def full_eo_list_actual_func():
    """чтение full_eo_list_actual"""
    full_eo_list_actual = pd.read_csv('data/full_eo_list_actual.csv', dtype=str)
    # level_1_df = pd.read_csv("data/level_1.csv", dtype=str)
    # full_eo_list_actual = pd.merge(full_eo_list_actual, level_1_df, on = 'level_1', how = 'left')
    full_eo_list_actual["operation_start_date"] = pd.to_datetime(full_eo_list_actual["operation_start_date"])
    full_eo_list_actual["operation_finish_date"] = pd.to_datetime(full_eo_list_actual["operation_finish_date"])
    full_eo_list_actual = full_eo_list_actual.astype({'strategy_id': int, 'avearage_day_operation_hours': float})

    return full_eo_list_actual


def full_eo_list_func():
    """чтение full_eo_list"""
    full_eo_list = pd.read_csv('data/full_eo_list.csv', dtype=str)
    full_eo_list["operation_start_date"] = pd.to_datetime(full_eo_list["operation_start_date"])
    full_eo_list["operation_finish_date"] = pd.to_datetime(full_eo_list["operation_finish_date"])
    full_eo_list = full_eo_list.astype({'strategy_id': int, 'avearage_day_operation_hours': float})

    return full_eo_list


def last_maint_date_func():
    last_maint_date = pd.read_csv('data/last_maint_date.csv')
    last_maint_date["last_maintanance_date"] = pd.to_datetime(last_maint_date["last_maintanance_date"],
                                                              format='%d.%m.%Y')

    return last_maint_date


def maintanance_jobs_df():
    """чтение maintanance_jobs_df"""
    maintanance_jobs_df = pd.read_csv('data/maintanance_jobs_df.csv', dtype=str)
    maintanance_jobs_df = maintanance_jobs_df.astype({'downtime_plan': float, "month_year_sort_index": int, "year":int, "month":int, "day": int, "hour":int})

    return maintanance_jobs_df


def maintanance_job_list_general_func():
    """чтение maintanance_job_list_general"""
    maintanance_job_list_general = pd.read_csv('data/maintanance_job_list_general.csv')
    maintanance_job_list_general = maintanance_job_list_general.astype({'downtime_planned': float, 'strategy_id': int})
    return maintanance_job_list_general


def eo_job_catologue_df_func():
    """чтение eo_job_catologue_df"""
    eo_job_catologue_df = pd.read_csv('data/eo_job_catologue.csv', dtype=str)
    eo_job_catologue_df["downtime_planned"] = eo_job_catologue_df["downtime_planned"].astype('float')
    eo_job_catologue_df["operation_start_date"] = pd.to_datetime(eo_job_catologue_df["operation_start_date"])
    eo_job_catologue_df["operation_finish_date"] = pd.to_datetime(eo_job_catologue_df["operation_finish_date"])

    return eo_job_catologue_df


def pass_interval_fill():
    '''создание списка pass interval в maintanance_job_list_general'''

    maintanance_job_list_general = maintanance_job_list_general_func()

    for index, row in maintanance_job_list_general.iterrows():
        pass_interval_temp = row['pass_interval']
        interval_motohours = int(row['interval_motohours'])

        if pass_interval_temp != 'not':
            pass_interval_list = pass_interval_temp.split(';')
            pass_interval_list = [int(i) for i in pass_interval_list]

            # в temp_list складываем значения, которые соответствуют original pass_interval_list
            temp_list = []
            for pass_interval_value in pass_interval_list:
                if pass_interval_value not in temp_list:
                    temp_list.append(pass_interval_value)

                temp_value = pass_interval_value
                # temp_list = []
                while temp_value < 135000:

                    if temp_value not in temp_list:
                        temp_list.append(temp_value)
                        temp_list.sort()
                    temp_value = temp_value + pass_interval_value
            #####################  Создаем список maintanance_interval #####################
            # next_go_interval - значение интервала проведения формы, которое будем итеративно считать
            next_go_interval = interval_motohours
            # go_interval_list  - список, в который будем складывать значения интервалов для проведения форм
            go_interval_list = []
            while next_go_interval < 135000:
                # если текущее значение next_go_interval не находится в temp_list (списке пропусков форм)
                # то добавляем значение в белый список
                if next_go_interval not in temp_list:
                    go_interval_list.append(next_go_interval)
                # прибавляем к текущему значению next_go_interval значение периодичности interval_motohours
                next_go_interval = next_go_interval + interval_motohours

            temp_list = [str(i) for i in temp_list]
            temp_string = ";".join(temp_list)
            maintanance_job_list_general.loc[index, ['pass_interval']] = temp_string

            go_interval_list = [str(i) for i in go_interval_list]
            go_interval_list_string = ";".join(go_interval_list)
            maintanance_job_list_general.loc[index, ['go_interval']] = go_interval_list_string
        else:
            maintanance_job_list_general.loc[index, ['go_interval']] = 'not'

    maintanance_job_list_general.to_csv('data/maintanance_job_list_general.csv', index=False)


###################################################################################################
def maintanance_category_prep():
    """Создание файла со списком категорий работ ТОИР"""
    df = maintanance_job_list_general_func()

    maintanance_category_id_list = []
    maintanance_category_id_df_list = []
    for index, row in df.iterrows():
        temp_dict = {}
        maintanance_category_id = row['maintanance_category_id']
        maintanance_name = row['maintanance_name']
        temp_dict['maintanance_category_id'] = maintanance_category_id
        temp_dict['maintanance_name'] = maintanance_name
        if maintanance_category_id not in maintanance_category_id_list:
            maintanance_category_id_list.append(maintanance_category_id)
            maintanance_category_id_df_list.append(temp_dict)

    df_result = pd.DataFrame(maintanance_category_id_df_list)
    df_result.to_csv('data/maintanance_category.csv', index=False)


#############################################################################################
def select_eo_for_calculation():
    """Выборка ео из полного списка full_eo_list_actual в full_eo_list"""
    full_eo_list_actual_df = full_eo_list_actual_func()
    # print(full_eo_list_actual_df)
    strategy_list_df = pd.read_csv('data/strategy_list.csv')
    strategy_list = strategy_list_df['strategy_id'].unique()
    eo_list_for_calculation = full_eo_list_actual_df.loc[full_eo_list_actual_df['strategy_id'].isin(strategy_list)]
    eo_list_for_calculation.to_csv('data/full_eo_list.csv', index=False)


#####################################################################################################
def eo_job_catologue():
    '''создание файла eo_job_catologue: список оборудование - работа на оборудовании'''
    # Джойним список машин из full_eo_list c планом ТО из maintanance_job_list_general
    maintanance_job_list_general_df = maintanance_job_list_general_func()

    maintanance_job_list_general_df.rename(columns={'upper_level_tehmesto_code': 'level_upper'}, inplace=True)
    full_eo_list = full_eo_list_func()
    eo_maintanance_plan_df = pd.merge(full_eo_list, maintanance_job_list_general_df, on='strategy_id', how='inner')

    # eo_maintanance_plan_df.to_csv('data/eo_maintanance_plan_df_delete.csv')

    # удаляем строки, в которых нет данных в колонке eo_main_class_code
    eo_maintanance_plan_df = eo_maintanance_plan_df.loc[eo_maintanance_plan_df['eo_main_class_code'] != 'no_data']

    # получаем первую букву в поле eo_class_code
    eo_maintanance_plan_df['check_S_eo_class_code'] = eo_maintanance_plan_df['eo_class_code'].astype(str).str[0]
    eo_maintanance_plan_df = eo_maintanance_plan_df.loc[eo_maintanance_plan_df['check_S_eo_class_code'] != 'S']

    eo_maintanance_plan_df['eo_maintanance_job_code'] = eo_maintanance_plan_df['eo_code'].astype(str) + '_' + \
                                                        eo_maintanance_plan_df['maintanance_code_id'].astype(str)

    eo_maintanance_plan_df = eo_maintanance_plan_df.loc[:,
                             ['eo_maintanance_job_code', 'strategy_id', 'eo_model_id', 'maintanance_code', 'eo_code',
                              'eo_main_class_code', 'eo_description', 'maintanance_category_id', 'maintanance_name',
                              'interval_type',
                              'interval_motohours', 'downtime_planned', 'pass_interval', 'go_interval',
                              'operation_start_date', 'operation_finish_date']].reset_index(drop=True)
    eo_job_catologue = eo_maintanance_plan_df

    eo_job_catologue.to_csv('data/eo_job_catologue.csv', index=False)

    ###################### ОБНОВЛЕНИЕ ДАННЫХ ФАЙЛА С ДАТОЙ СТАРТА РАБОТ. ####################################
    # если в файле last_maint_date нет строки с кодом eo_код формы, то добавляем строку в файл. Указываем дату по умолчанию 31.12.2022
    # список кодов в файле last_maint_date
    last_maint_date = pd.read_csv('data/last_maint_date.csv')
    last_maint_date_eo_maintanance_job_code_list = last_maint_date['eo_maintanance_job_code'].unique()
    # список кодов в файле eo_job_catologue
    eo_job_catologue_eo_maintanance_job_code_list = eo_job_catologue['eo_maintanance_job_code'].unique()

    # итерируемся по eo_job_catologue_eo_maintanance_job_code_list
    # если значение нет в списке last_maint_date_eo_maintanance_job_code_list то добавляем строку
    last_maint_date_eo_maintanance_job_code_update = []
    for eo_maintanance_job_code in eo_job_catologue_eo_maintanance_job_code_list:
        temp_dict = {}
        temp_dict['eo_maintanance_job_code'] = eo_maintanance_job_code
        temp_dict['last_maintanance_date'] = '31.12.2022'
        if eo_maintanance_job_code not in last_maint_date_eo_maintanance_job_code_list:
            last_maint_date_eo_maintanance_job_code_update.append(temp_dict)

    last_maint_date_eo_maintanance_job_code_update_df = pd.DataFrame(last_maint_date_eo_maintanance_job_code_update)
    last_maint_date_updated_df = pd.concat([last_maint_date, last_maint_date_eo_maintanance_job_code_update_df])
    last_maint_date_updated_df.to_csv('data/last_maint_date.csv', index=False)

    return eo_job_catologue


##################################################################################################
def maintanance_jobs_df_prepare():
    '''подготовка файла со списком работ - основной файл для построения графика простоев'''

    # читаем файл eo_job_catologue
    eo_job_catologue_df = eo_job_catologue_df_func()
    last_day_of_selection = initial_values.last_day_of_selection
    ##########################################################
    ##########################################################
    ##########################################################
    ############### Для тестрования возьмем всего три строки
    # eo_job_catologue_df = eo_job_catologue_df.loc[eo_job_catologue_df['eo_maintanance_job_code'].isin(['100000084492_36'])]
    # eo_job_catologue_df = eo_job_catologue_df.loc[eo_job_catologue_df['eo_maintanance_job_code'].isin(['100000084492_47'])]
    # eo_job_catologue_df = eo_job_catologue_df.loc[eo_job_catologue_df['eo_maintanance_job_code'].isin(['100000084492_37'])]
    eo_job_catologue_df = eo_job_catologue_df.loc[
        eo_job_catologue_df['eo_maintanance_job_code'].isin(['100000084492_47', '100000084492_37'])]
    full_eo_list = full_eo_list_func()

    # выдергиваем из full_eo_list 'eo_code', 'avearage_day_operation_hours'
    full_eo_list_selected = full_eo_list.loc[:, ['eo_code', 'avearage_day_operation_hours']]

    # джойним с full_eo_list
    eo_maint_plan_with_dates_with_full_eo_list = pd.merge(eo_job_catologue_df, full_eo_list_selected, on='eo_code',
                                                          how='left')

    # джйоним с файлом last_maint_date - датами проведени последней формы.
    # принимаем, что дата последней формы - это дата начала эксплуатации. От этой даты начинаем отсчет
    last_maint_date = last_maint_date_func()
    eo_maint_plan = pd.merge(eo_maint_plan_with_dates_with_full_eo_list, last_maint_date, on='eo_maintanance_job_code',
                             how='left')

    # eo_maint_plan.to_csv('data/eo_maint_plan_delete.csv')
    # в maintanance_jobs_result_list будем складывать дикты с записями о сгенерированных ТО-шках.
    maintanance_jobs_result_list = []

    for row in eo_maint_plan.itertuples():
        # print(row)
        maintanance_job_code = getattr(row, "eo_maintanance_job_code")
        eo_code = getattr(row, "eo_code")
        standard_interval_motohours = float(getattr(row, "interval_motohours"))
        plan_downtime = getattr(row, "downtime_planned")
        start_point = getattr(row, "last_maintanance_date")
        operation_start_date = getattr(row, "operation_start_date")
        operation_finish_date = getattr(row, "operation_finish_date")
        avearage_day_operation_hours = float(getattr(row, "avearage_day_operation_hours"))
        maintanance_category_id = getattr(row, "maintanance_category_id")
        maintanance_name = getattr(row, "maintanance_name")
        interval_type = getattr(row, "interval_type")
        pass_interval = getattr(row, "pass_interval")
        go_interval = getattr(row, "go_interval")

        # maintanance_start_datetime = start_point
        # если это ежедневное обслуживание, то расставляем через каждые 24 часа
        if maintanance_category_id == 'eto':
            # если у нас ежедневное ТО, то это особый случай. переписывем точку старта
            start_point = initial_values.eto_start_point
            maintanance_start_datetime = start_point
            while maintanance_start_datetime < last_day_of_selection:
                temp_dict = {}
                temp_dict['maintanance_job_code'] = maintanance_job_code
                temp_dict['eo_code'] = eo_code
                temp_dict['interval_motohours'] = standard_interval_motohours
                temp_dict['interval_type'] = interval_type
                temp_dict['maint_interval'] = 24
                temp_dict['downtime_plan'] = plan_downtime
                temp_dict['maintanance_start_datetime'] = maintanance_start_datetime

                maintanance_finish_datetime = maintanance_start_datetime + timedelta(hours=plan_downtime)
                temp_dict['maintanance_finish_datetime'] = maintanance_finish_datetime
                temp_dict['maintanance_date'] = maintanance_start_datetime.date()
                temp_dict['maintanance_category_id'] = maintanance_category_id
                temp_dict['maintanance_name'] = maintanance_name
                temp_dict['avearage_day_operation_hours'] = avearage_day_operation_hours

                maintanance_start_datetime = maintanance_start_datetime + timedelta(hours=24)

                if maintanance_start_datetime >= operation_start_date and maintanance_start_datetime <= operation_finish_date:
                    maintanance_jobs_result_list.append(temp_dict)

        # если у формы нет поглащений другими формами, то расставляем через каждый интервал между формами
        elif maintanance_category_id != 'eto' and pass_interval == 'not':
            maintanance_start_datetime = start_point

            while maintanance_start_datetime < last_day_of_selection:
                temp_dict = {}
                temp_dict['maintanance_job_code'] = maintanance_job_code
                temp_dict['eo_code'] = eo_code
                temp_dict['interval_motohours'] = standard_interval_motohours
                temp_dict['maint_interval'] = standard_interval_motohours
                temp_dict['downtime_plan'] = plan_downtime
                temp_dict['maintanance_start_datetime'] = maintanance_start_datetime
                maintanance_finish_datetime = maintanance_start_datetime + timedelta(hours=plan_downtime)
                temp_dict['maintanance_finish_datetime'] = maintanance_finish_datetime
                temp_dict['maintanance_date'] = maintanance_start_datetime.date()
                temp_dict['maintanance_category_id'] = maintanance_category_id
                temp_dict['maintanance_name'] = maintanance_name
                # количество суток, которые требуются для того, чтобы выработать интервал до следующей формы
                number_of_days_to_next_maint = standard_interval_motohours // avearage_day_operation_hours
                # остаток часов в следующие сутки для выработки интервала до следующей формы
                remaining_hours = standard_interval_motohours - number_of_days_to_next_maint * avearage_day_operation_hours
                # календарный интервал между формами = кол-во суток х 24 + остаток
                calendar_interval_between_maint = number_of_days_to_next_maint * 24 + remaining_hours

                ############## В зависимости от типа межсервисного интервала определяем момент следующего ТО ##################
                next_maintanance_datetime = maintanance_start_datetime + timedelta(
                    hours=calendar_interval_between_maint) + timedelta(hours=plan_downtime)
                days_between_maintanance = next_maintanance_datetime - maintanance_start_datetime
                # Если интервал задан в часах, то переписываем значения
                if interval_type == 'hrs':
                    next_maintanance_datetime = maintanance_start_datetime + timedelta(
                        hours=standard_interval_motohours) + timedelta(hours=plan_downtime)
                    days_between_maintanance = next_maintanance_datetime - maintanance_start_datetime

                temp_dict['days_between_maintanance'] = days_between_maintanance
                temp_dict['next_maintanance_datetime'] = next_maintanance_datetime

                if maintanance_start_datetime >= operation_start_date and maintanance_start_datetime <= operation_finish_date:
                    maintanance_jobs_result_list.append(temp_dict)
                    maintanance_start_datetime = next_maintanance_datetime

        # остаются записи, которые не ЕТО, и у которых есть поглащения форм.
        # для таких записей итерируемся по списку 'go interval'
        elif go_interval != 'not':
            go_interval_list = go_interval.split(';')
            go_interval_list = [int(i) for i in go_interval_list]

            # base_start_maintanance_datetime - это дата к которой будем прибавлять все интервалы из цикла периодов
            base_start_maintanance_datetime = start_point

            # итерируемся по списку go_interval
            for maintanance_interval_temp in go_interval_list:
                # количество суток, которые требуются для того, чтобы выработать интервал до следующей формы
                number_of_days_to_next_maint = maintanance_interval_temp // avearage_day_operation_hours
                # остаток часов в следующие сутки для выработки интервала до следующей формы
                remaining_hours = maintanance_interval_temp - number_of_days_to_next_maint * avearage_day_operation_hours
                # календарный интервал между формами = кол-во суток х 24 + остаток
                calendar_interval_between_maint = number_of_days_to_next_maint * 24 + remaining_hours
                maintanance_start_datetime = base_start_maintanance_datetime + timedelta(
                    hours=calendar_interval_between_maint) + timedelta(hours=plan_downtime)
                maintanance_finish_datetime = maintanance_start_datetime + timedelta(hours=plan_downtime)
                temp_dict = {}
                temp_dict['maintanance_job_code'] = maintanance_job_code
                temp_dict['eo_code'] = eo_code
                temp_dict['interval_motohours'] = standard_interval_motohours
                temp_dict['downtime_plan'] = plan_downtime
                temp_dict['maintanance_start_datetime'] = maintanance_start_datetime
                temp_dict['maintanance_finish_datetime'] = maintanance_finish_datetime
                temp_dict['maintanance_start_date'] = maintanance_start_datetime.date()
                temp_dict['maintanance_category_id'] = maintanance_category_id
                temp_dict['maintanance_name'] = maintanance_name

                temp_dict['maint_interval'] = maintanance_interval_temp
                temp_dict['pass_interval_list'] = pass_interval
                temp_dict['go_interval_list'] = go_interval
                next_maintanance_datetime = maintanance_start_datetime + timedelta(
                    hours=calendar_interval_between_maint) + timedelta(hours=plan_downtime)
                days_between_maintanance = next_maintanance_datetime - maintanance_start_datetime
                temp_dict['days_between_maintanance'] = days_between_maintanance
                temp_dict['next_maintanance_datetime'] = next_maintanance_datetime
                if maintanance_start_datetime >= operation_start_date and maintanance_start_datetime <= operation_finish_date:
                    maintanance_jobs_result_list.append(temp_dict)

    maintanance_jobs_df = pd.DataFrame(maintanance_jobs_result_list)
    # maintanance_jobs_df.to_csv('data/maintanance_jobs_df_full_list_delete.csv')

    # режем то, что получилось в период три года
    maintanance_jobs_df = maintanance_jobs_df.loc[
        maintanance_jobs_df['maintanance_start_datetime'] >= first_day_of_selection]
    maintanance_jobs_df = maintanance_jobs_df.loc[
        maintanance_jobs_df['maintanance_start_datetime'] <= last_day_of_selection]

    ############# прицепляем eo_model_id #############################
    eo_model_id_eo_list = full_eo_list.loc[:, ['eo_code', 'eo_model_id', 'eo_model_name', 'level_upper']]
    maintanance_jobs_df = pd.merge(maintanance_jobs_df, eo_model_id_eo_list, on='eo_code', how='left')

    maintanance_jobs_df['maintanance_date'] = maintanance_jobs_df['maintanance_start_datetime'].astype(str)
    maintanance_jobs_df['year'] = maintanance_jobs_df['maintanance_start_datetime'].dt.year
    maintanance_jobs_df['month'] = maintanance_jobs_df['maintanance_start_datetime'].dt.month
    maintanance_jobs_df['day'] = maintanance_jobs_df['maintanance_start_datetime'].dt.day
    maintanance_jobs_df['hour'] = maintanance_jobs_df['maintanance_start_datetime'].dt.hour
    maintanance_jobs_df['month_year'] = maintanance_jobs_df['month'].astype('str') + "_" + maintanance_jobs_df[
        'year'].astype('str')
    sort_index_month_year = {'1_2023': 1, '2_2023': 2, '3_2023': 3, '4_2023': 4, '5_2023': 5, '6_2023': 6, '7_2023': 7,
                             '8_2023': 8, '9_2023': 9, '10_2023': 10, '11_2023': 11, '12_2023': 12, '1_2024': 13,
                             '2_2024': 14, '3_2024': 15, '4_2024': 16, '5_2024': 17, '6_2024': 18, '7_2024': 19,
                             '8_2024': 20, '9_2024': 21, '10_2024': 22, '11_2024': 23, '12_2024': 24, '1_2025': 25,
                             '2_2025': 26, '3_2025': 27, '4_2025': 28, '5_2025': 29, '6_2025': 30, '7_2025': 31,
                             '8_2025': 32, '9_2025': 33, '10_2025': 34, '11_2025': 35, '12_2025': 36}

    maintanance_jobs_df['month_year_sort_index'] = maintanance_jobs_df['month_year'].map(sort_index_month_year)

    level_upper = pd.read_csv('data/level_upper.csv')

    # джойним с level_upper
    maintanance_jobs_df = pd.merge(maintanance_jobs_df, level_upper, on='level_upper', how='left')
    # создаем поле-ключ teh-mesto-month-year

    maintanance_jobs_df['teh_mesto_month_year'] = maintanance_jobs_df['level_upper'] + '_' + maintanance_jobs_df[
        'month_year']

    maintanance_jobs_df['maintanance_jobs_id'] = maintanance_jobs_df['eo_code'].astype(str) + "_" + maintanance_jobs_df[
        'maintanance_category_id'].astype(str) + "_" + maintanance_jobs_df['maintanance_start_datetime'].astype(str)
    maintanance_jobs_df.sort_values(by=['maintanance_start_datetime'], ignore_index = True, inplace=True)

    maintanance_jobs_df.to_csv('data/maintanance_jobs_df.csv', index=False)

    return maintanance_jobs_df


# заполняем календарный фонд по оборудованию
# берем машины, кооторые участвуют в файле eo_job_catologue.csv
def fill_calendar_fond():
    eo_list_under_maintanance_program = pd.read_csv('data/eo_job_catologue.csv', dtype=str)
    # new data frame with split value columns
    # new = eo_list_under_maintanance_program['eo_code'].str.split(".", n = 1, expand = True)
    # making separate first name column from new data frame
    # eo_list_under_maintanance_program["eo_code"]= new[0]

    eo_list = eo_list_under_maintanance_program['eo_code'].unique()

    result_list = []
    # итерируемся по списку еo
    for eo in eo_list:
        maint_date = first_day_of_selection
        while maint_date < last_day_of_selection:
            temp_dict = {}
            temp_dict['eo_code'] = eo
            temp_dict['datetime'] = maint_date
            temp_dict['calendar_fond'] = 24
            result_list.append(temp_dict)
            maint_date = maint_date + timedelta(hours=24)

    eo_calendar_fond = pd.DataFrame(result_list)


###################### РАСЧЕТ КАЛЕНДАРНОГО ФОНДА И ПРОСТОЕВ ПО ЧАСАМ НА ТРИ ГОДА ######################
def hour_calculation():
  """РАСЧЕТ КАЛЕНДАРНОГО ФОНДА И ПРОСТОЕВ ПО ЧАСАМ НА ТРИ ГОДА"""
  # необходимо получить дефолтную таблицу с нулями
  # Для этого берем начальную точку в нуле часов 1 января 2023 года, прибавляем час и записываем новую строку
  start_point = pd.to_datetime('01.01.2023', format='%d.%m.%Y')

  # Список ЕО для почасовой модели
  full_eo_list = full_eo_list_func()
  # full_eo_list.to_csv('data/full_eo_list_delete.csv')
  full_eo_list = full_eo_list.loc[:, ['eo_code', 'operation_start_date', 'operation_finish_date']]

  ###################  ОГРАНИЧИМСЯ ДЛЯ ТЕСТИРОВАНИЯ ОДНОЙ МАШИНОЙ И ОДНИМ ГОДОМ #################
  eo_list = full_eo_list.loc[full_eo_list['eo_code'] == '100000084492']
  # eo_list.to_csv('data/eo_list_delete.csv')
  # operation_finish_date = pd.to_datetime('31.12.2023', format='%d.%m.%Y')
  # eo_list = full_eo_list
  # print(eo_list)
  # eo_list = full_eo_list.loc[:, ['eo_code', 'operation_start_date', 'operation_finish_date']]

  result_df_list = []
  for row in eo_list.itertuples():
      temp_dict = {}
      eo_code = getattr(row, "eo_code")
      operation_start_date = getattr(row, "operation_start_date")
      operation_finish_date = getattr(row, "operation_finish_date")
      current_hour = start_point
      
      while current_hour < last_day_of_selection:
          temp_dict['eo_code'] = eo_code
          temp_dict['model_hour'] = current_hour
          temp_dict['year'] = current_hour.year
          temp_dict['month'] = current_hour.month
          temp_dict['month_year'] = str(current_hour.month) + "_" + str(current_hour.year)
          

          ################ если текущее значение часа внутри времени эксплуатации машины, то ставим единичку в календарный фонд времени #################
          if current_hour > operation_start_date and current_hour < operation_finish_date:
              temp_dict['calendar_fond_status'] = 1
          else:
              temp_dict['calendar_fond_status'] = 0

          temp_dict['downtime_status'] = 0

          result_df_list.append(temp_dict)
          current_hour = current_hour + timedelta(hours=1)
          temp_dict = {}

  model_hours_df = pd.DataFrame(result_df_list)

  # print("model_hours_df info: ", model_hours_df.info())
  # model_hours_df.to_csv('data/model_hours_df_delete.csv')

  # ПРОСТОИ. Нужно итерировать по таблице с простоями. Получать из нее ЕО момент начала ремонта и величину простоя
  # определить момент окончания. Затем отрезать мастер таблицу по этому периоду и поместить в поле простоя единички
  maintanance_jobs_df = maintanance_jobs_df_prepare()
  maintanance_jobs_df_selected = maintanance_jobs_df.loc[:,
                                 ['maintanance_jobs_id', 'eo_code','maintanance_category_id', 'maintanance_name', 'maintanance_start_datetime', 'maintanance_finish_datetime', 'downtime_plan']]
  maintanance_jobs_df_selected.to_csv('data/maintanance_jobs_df_selected_delete.csv', index = False)

  # maintanance_jobs_df_selected = maintanance_jobs_df_selected.loc[maintanance_jobs_df_selected["maintanance_jobs_id"] == '100000084492_tr_2023-02-08 05:36:00']

  for row in maintanance_jobs_df_selected.itertuples():
    maintanance_jobs_id = getattr(row, "maintanance_jobs_id")
    # print(maintanance_jobs_id)
    eo_code = getattr(row, "eo_code")
    maintanance_name = getattr(row, "maintanance_name")
    maintanance_category_id = getattr(row, "maintanance_category_id")
    
    maintanance_start_datetime = getattr(row, "maintanance_start_datetime")
    maintanance_finish_datetime = getattr(row, "maintanance_finish_datetime")
    downtime_plan = getattr(row, "downtime_plan")

    # print("maintanance_start_datetime", maintanance_start_datetime)
    # print("maintanance_finish_datetime", maintanance_finish_datetime)
    # Режем таблицу с почасовыми строками по моменту старта и завершения работы
    model_hours_df_cut_by_maint_job = model_hours_df.loc[
          (model_hours_df['model_hour'] >= maintanance_start_datetime) &
          (model_hours_df['model_hour'] <= maintanance_finish_datetime)]

    # print(model_hours_df_cut_by_maint_job)
    # indexes - список индексов записей в которых надо поставить единичку, то есть в этих записях есть простой
    indexes = model_hours_df_cut_by_maint_job.index.values

    model_hours_df_cut_by_maint_job = model_hours_df_cut_by_maint_job.copy()
    model_hours_df.loc[indexes, ['maintanance_jobs_id']] = maintanance_jobs_id
    ##### Записываем единичку в основную таблицу
    model_hours_df.loc[indexes, ['downtime_status']] = 1

    # print(model_hours_df_cut_by_maint_job)
  model_hours_df.to_csv('data/model_3y_hours_df.csv', index=False)

  # Готовим таблицу для КТГ
  # maintanance_jobs__for_zero_dowtime.groupby(['teh_mesto_month_year', 'level_upper', 'Название технического места', 'month_year', 'year'], as_index=False)['dowtime_plan, hours'].sum()
  model_hours_ktg_data = model_hours_df.groupby(['month_year'], as_index = False)[['calendar_fond_status', 'downtime_status']].sum()
  model_hours_ktg_data['ktg'] = (model_hours_ktg_data['calendar_fond_status'] - model_hours_ktg_data['downtime_status']) / model_hours_ktg_data['calendar_fond_status']
  
  model_hours_ktg_data['ktg'] = model_hours_ktg_data['ktg'].apply(lambda x: round(x, 2))
  period_dict = initial_values.period_dict
  
  period_sort_index = initial_values.period_sort_index

  model_hours_ktg_data['period'] = model_hours_ktg_data['month_year'].map(period_dict).astype(str)

  model_hours_ktg_data['period_sort_index'] = model_hours_ktg_data['month_year'].map(period_sort_index)
  model_hours_ktg_data.sort_values(by='period_sort_index', inplace = True)
  
  ktg_table_data = model_hours_ktg_data.loc[:, ['period', 'calendar_fond_status', 'downtime_status', 'ktg']]
  ktg_table_data = ktg_table_data.rename(columns={'period': 'Период', 'calendar_fond_status': 'Календарный фонд, час', 'downtime_status': 'Запланированный простой, час', 'ktg': 'Запланированный КТГ'})

  ktg_table_data.to_csv('data/model_hours_ktg_data.csv', index = False)

  downtime_graph_data = ktg_table_data.loc[:, ['Период','Запланированный простой, час']]
  downtime_graph_data.to_csv('widget_data/downtime_graph_data.csv', index = False)




def ktg_by_month_models():
    maintanance_jobs_df = maintanance_jobs_df_prepare()
    eo_calendar_fond = fill_calendar_fond()
    year = 2023

    maintanance_jobs__for_zero_dowtime = maintanance_jobs_df.loc[:,
                                         ['teh_mesto_month_year', 'level_upper', 'Название технического места',
                                          'month_year', 'year']]
    maintanance_jobs__for_zero_dowtime['downtime_plan'] = 0
    maintanance_jobs__for_zero_dowtime_groupped = maintanance_jobs__for_zero_dowtime.groupby(
        ['teh_mesto_month_year', 'level_upper', 'Название технического места', 'month_year', 'year'], as_index=False)[
        'downtime_plan'].sum()

def total_qty_EO():
  """расчет количества машин в выборке для отображения в карточке 2023 года"""
  # Читаем maintanance_jobs_df()
  maintanance_jobs_dataframe = maintanance_jobs_df()
  maintanance_jobs_dataframe_2023 = maintanance_jobs_dataframe.loc[maintanance_jobs_dataframe['year'] == 2023]
  maintanance_jobs_dataframe_2024 = maintanance_jobs_dataframe.loc[maintanance_jobs_dataframe['year'] == 2024]
  maintanance_jobs_dataframe_2025 = maintanance_jobs_dataframe.loc[maintanance_jobs_dataframe['year'] == 2025]
  # Считаем кол-во записей в колонке eo_code
  eo_qty_2023 = len(maintanance_jobs_dataframe_2023['eo_code'].unique())
  eo_qty_2024 = len(maintanance_jobs_dataframe_2024['eo_code'].unique())
  eo_qty_2025 = len(maintanance_jobs_dataframe_2025['eo_code'].unique())
  return eo_qty_2023, eo_qty_2024, eo_qty_2025


def eo_list_download_preparation():
  """подготовка csv файла для выгрузки в эксель данных о машинах в выборке"""
  # Читаем maintanance_jobs_df()
  maintanance_jobs_dataframe = maintanance_jobs_df()
  # извлекаем список ЕО
  eo_list = pd.DataFrame(list(set(maintanance_jobs_dataframe['eo_code'])), columns=['eo_code'])
  # джойним с full_eo_list 
  full_eo_list = full_eo_list_func()
  eo_list_data = pd.merge(eo_list, full_eo_list, on = 'eo_code', how ='left')

  # выбираем колонки
  eo_list_data = eo_list_data.loc[:, ['level_1_description','eo_class_description','constr_type','teh_mesto',	'mvz','eo_model_name', 'eo_code',	 'eo_description',  'operation_start_date', 'operation_finish_date', 'avearage_day_operation_hours_updated', 'Наработка 1.03.2022']]
  eo_list_data['eo_code'] = eo_list_data['eo_code'].astype(str)
  print(eo_list_data['avearage_day_operation_hours_updated'])

  # переименовываем колонки
  eo_download_data = eo_list_data.rename(columns={'level_1_description':"БЕ", 'eo_class_description':"Класс ЕО", "constr_type": "Тип конструкции", "teh_mesto": "Техместо",'mvz':"МВЗ", "eo_model_name": "Модель ЕО", "eo_code": "ЕО", "eo_description": "Наименоваание ЕО", "operation_start_date":"Дата начала эксплуатации", "operation_finish_date": "Дата завершения эксплуатации", "avearage_day_operation_hours_updated": "Среднесуточная наработка"})


  
  eo_download_data.to_csv('widget_data/eo_download_data.csv', index = False)

eo_list_download_preparation()

# total_qty_EO_2023()
################# ЗАПУСК ФУНКЦИЙ #############################


# full_eo_list_actual_func()
# select_eo_for_calculation()
# full_eo_list_func()
# last_maint_date_func()
# functions.pass_interval_fill() '''создание списка pass interval в maintanance_job_list_general'''
# pass_interval_fill()
  

# functions.maintanance_category_prep() """Создание файла со списком категорий работ ТОИР"""
# maintanance_category_prep()


# functions.eo_job_catologue():'''создание файла eo_job_catologue: список оборудование - работа на оборудовании'''
# eo_job_catologue()


# maintanance_jobs_df_prepare()
# maintanance_jobs_df()
# fill_calendar_fond()

# hour_calculation()
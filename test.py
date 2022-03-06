import pandas as pd
import functions

full_eo_list_actual = functions.full_eo_list_actual_func()

eo_list = full_eo_list_actual.loc[full_eo_list_actual['eo_model_id'] != 'no_data']

eo_list = eo_list.loc[:, ['level_1_description', 'eo_code',	'eo_model_name', 'eo_class_description', 'eo_description',	'teh_mesto', 'operation_start_date', 'constr_type']]



eo_list.rename(columns={'level_1_description': 'БЕ', 'eo_code':'EO', 'eo_model_name': 'Модель оборудования', 'eo_class_description': 'класс ео', 'eo_description':'Наименование оборудования', 'teh_mesto': 'техместо', 'operation_start_date': 'Дата начала эксплуатации', 'constr_type': 'Тип конструкции'}, inplace=True)
# eo_list.to_csv('data/eo_list_temp.csv', index = False)

teh_karta_spisok = pd.read_csv('data/teh_karta_spisok.csv', dtype = str)


teh_karta_spisok = teh_karta_spisok.loc[:, ['Тип техкарты', 'Группа', 'СчтГрупТехкарт', 'Описание', 'Гр. плановиков', 'Стратегия', 'Метка удаления', 'Монтажный узел', 'Статус', 'Дата изменения', 'Дата создания', 'Действит. с']]

teh_karta_spisok.rename(columns={'Монтажный узел': 'Тип конструкции'}, inplace=True)

teh_karta_spisok = teh_karta_spisok.loc[teh_karta_spisok['Метка удаления'] != 'X']
teh_karta_spisok = teh_karta_spisok.loc[teh_karta_spisok['Статус'] == '4']
teh_karta_spisok["Дата изменения"] = pd.to_datetime(teh_karta_spisok["Дата изменения"], format='%m/%d/%Y')
teh_karta_spisok["Дата создания"] = pd.to_datetime(teh_karta_spisok["Дата создания"], format='%m/%d/%Y')
teh_karta_spisok["Действит. с"] = pd.to_datetime(teh_karta_spisok["Действит. с"], format='%m/%d/%Y')

teh_karta_spisok.to_csv('data/teh_karta_spisok_selected.csv', index = False)

################### объединяем тех карты и ео ############################

eo_teh_karta_df = pd.merge(eo_list, teh_karta_spisok, on = 'Тип конструкции', how = 'left')

eo_teh_karta_df.to_csv('data/eo_teh_karta_df.csv', index = False)


################### СУЩЕСТВУЮЩИЕ ПЛАНЫ ТОРО ############################
plans_toro_df = pd.read_csv('data/plans_toro.csv', dtype = str)
plans_toro_df['strategy_str'] = plans_toro_df['strategy'].astype(str) + "_str"


plans_toro_df['updated-counter']  = plans_toro_df['СчетГруппТехкарт'].astype(str)

# print(plans_toro_df['updated-counter'])
# список счетчиков, которые нужно заменить в строках планов
update_counter_dict = {"48": 'Д2',"40":'Д1'}
# plans_toro_df['updated-counter'] = plans_toro_df['СчетГруппТехкарт'].map(update_counter_dict)
plans_toro_df['updated-counter'].map(update_counter_dict)

plans_toro_df.to_csv('data/plans_toro_delete.csv', index = False)

plans_toro_df['strategy_str_counter'] = plans_toro_df['strategy_str'].astype(str) + plans_toro_df['updated-counter'].astype(str)




# print(plans_toro_df['strategy_str])
							
plans_toro_df_selected = plans_toro_df.loc[:, ['ПозПредупредТОРО', 'ПланПредупрТОРО', 'Позиция предупред. ТОРО - описание', 'Группа плановиков', 'Единица оборудования', 'Вид работы ТОРО', 'Вид заказа', 'Тип техкарты', 'Группа','СчетГруппТехкарт', 'updated-counter', 'strategy_str_counter']]
# plans_toro_df_selected['Страт. предупр. ТОРО'] = plans_toro_df_selected['Страт. предупр. ТОРО'].astype(str)
plans_toro_df_selected.to_csv('data/plans_toro_df_selected.csv', index = False)

plans_toro_df_selected.rename(columns={'Единица оборудования': 'EO'}, inplace=True)


# plans_toro_df_selected['код_цикла'] = plans_toro_df_selected['strategy_str'].astype(str) + plans_toro_df_selected['СчетГруппТехкарт'].astype(str)


eo_plan_toro_df = pd.merge(plans_toro_df_selected, eo_list, on = 'EO', how = 'left')


# читаем файл стратегии- формы
strategy_forms_df = pd.read_csv('data/strategy_forms.csv')
strategy_forms_df['strategy_str'] = strategy_forms_df['Стратегия'].astype(str) + "_str"
strategy_forms_df['strategy_str_counter'] = strategy_forms_df['strategy_str'].astype(str) + strategy_forms_df['КраткНазвЦикла'].astype(str)
					
strategy_forms_df_selected = strategy_forms_df.loc[:, ['Название стратерии', 'Единица', 'Текст цикла ПредупрТОРО', 'КраткНазвЦикла', 'Цикл', 'код_цикла', 'strategy_str_counter']]
strategy_forms_df_selected.to_csv('data/strategy_forms_df_selected_delete.csv')

# объединяем планы и стратегии
eo_plan_toro_strategy_df = pd.merge(eo_plan_toro_df, strategy_forms_df_selected, on = 'strategy_str_counter', how = 'left')

eo_plan_toro_strategy_df.to_csv('data/eo_plan_toro_strategy_df.csv', index = False)

# объединяем техкарты и стратегии
eo_teh_carts_toro_strategy_df = pd.merge(eo_teh_karta_df, strategy_forms_df, on = 'Стратегия', how = 'left')
eo_teh_carts_toro_strategy_df.to_csv('data/eo_teh_carts_toro_strategy_df.csv', index = False)
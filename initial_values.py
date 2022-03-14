import pandas as pd

first_day_of_selection = pd.to_datetime('01.01.2023', format='%d.%m.%Y')
last_day_of_selection = pd.to_datetime('01.01.2026', format='%d.%m.%Y')
eto_start_point = pd.to_datetime('01.01.2023_8', format='%d.%m.%Y_%H')

period_dict = {'1_2023': "янв 2023", '2_2023': "фев 2023", '3_2023': "мар 2023", '4_2023': "апр 2023", '5_2023': "май 2023", '6_2023': "июн 2023", '7_2023': "июл 2023", '8_2023': "авг 2023", '9_2023': "сен 2023", '10_2023': "окт 2023", '11_2023': "ноя 2023", '12_2023': "дек 2023", '1_2024': "янв 2024", '2_2024': "фев 2024", '3_2024': "мар 2024", '4_2024': "апр 2024", '5_2024': "май 2024", '6_2024': "июн 2024", '7_2024': "июл 2024", '8_2024': "авг 2024", '9_2024': "сен 2024", '10_2024': "окт 2024", '11_2024': "ноя 2024", '12_2024': "дек 2024", '1_2025': "янв 2025", '2_2025': "фев 2025", '3_2025': "мар 2025", '4_2025': "апр 2025", '5_2025': "май 2025", '6_2025': "июн 2025", '7_2025': "июл 2025", '8_2025': "авг 2025", '9_2025': "сен 2025", '10_2025': "окт 2025", '11_2025': "ноя 2025", '12_2025': "дек 2025"}

period_sort_index = {'1_2023':1, '2_2023': 2, '3_2023': 3, '4_2023': 4, '5_2023': 5, '6_2023': 6, '7_2023': 7, '8_2023': 8, '9_2023': 9, '10_2023': 10, '11_2023': 11, '12_2023': 12, '1_2024':13, '2_2024': 14, '3_2024': 15, '4_2024': 16, '5_2024': 17, '6_2024': 18, '7_2024': 19, '8_2024': 20, '9_2024': 21, '10_2024': 22, '11_2024': 23, '12_2024': 24, '1_2025':25, '2_2025': 26, '3_2025': 27, '4_2025': 28, '5_2025': 29, '6_2025': 30, '7_2025': 31, '8_2025': 32, '9_2025': 33, '10_2025': 34, '11_2025': 35, '12_2025': 36}

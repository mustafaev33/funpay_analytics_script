import pandas as pd
from dateparser import parse
from rich.console import Console
from __main__ import TEXTS

console = Console()

def analyze_dates(df, currency):
    console.print(TEXTS['date_analyzer'])

    df['Дата_время'] = df['Дата'].apply(lambda x: parse(x, languages=['ru']))
    df_valid = df.dropna(subset=['Дата_время'])
    df_valid['Цена'] = pd.to_numeric(df_valid['Цена'], errors='coerce')

    console.print(TEXTS['an_data_notes'].format(len(df_valid), len(df)))

    console.print(TEXTS['sls_by_month'])
    monthly = df_valid.groupby(df_valid['Дата_время'].dt.to_period('M')).agg(
        Продаж=('Цена', 'count'),
        Выручка=('Цена', 'sum')
    )
    console.print(monthly)

    console.print(TEXTS['sls_week'])
    days = df_valid['Дата_время'].dt.day_name()
    console.print(days.value_counts().sort_index())
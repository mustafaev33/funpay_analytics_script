import pandas as pd
from dateparser import parse

def analyze_dates(df, currency):
    print("Date analyzer:")

    df['Дата_время'] = df['Дата'].apply(lambda x: parse(x, languages=['ru']))
    df_valid = df.dropna(subset=['Дата_время'])

    print(f"Analyzed {len(df_valid)} of {len(df)} data-notes")

    print("\nSales by month: ")
    monthly = df_valid.groupby(df_valid['Дата_время'].dt.to_period('M')).agg(
        Продаж=('Цена', 'count'),
        Выручка=('Цена', 'sum')
    )
    print(monthly)

    print("\nSales by day of the week: ")
    
    days = df_valid['Дата_время'].dt.day_name()
    print(days.value_counts().sort_index())
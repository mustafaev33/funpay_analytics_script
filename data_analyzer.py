import pandas as pd
import os
from datetime_analyzer import analyze_dates
from visual import visual_data
from rich.console import Console
from __main__ import TEXTS

console = Console()

def run_data_analytics():
    csv_exists = os.path.exists("my_sales.csv")
    xlsx_exists = os.path.exists("my_sales.xlsx")

    console.print(TEXTS['load_data'])

    if csv_exists:
        df = pd.read_csv("my_sales.csv", encoding="utf-8-sig")
    elif xlsx_exists:
        df = pd.read_excel("my_sales.xlsx", engine='openpyxl')
    else:
        console.print(TEXTS['data_error'])
        return
    

    currency = df['Валюта'].mode()[0] if 'Валюта' in df.columns else '₽'
    console.print(TEXTS['rec_upload'].format(len(df)))
    console.print(TEXTS['fin_sum'])

    df['Цена'] = pd.to_numeric(df['Цена'], errors='coerce')

    total_revenue = df['Цена'].sum()
    avg_check = df['Цена'].mean()
    total_deals = len(df)

    closed_deals = df[df['Статус'] == 'Закрыт']
    refund_deals = df[df['Статус'] == 'Возврат']

    closed_count = len(closed_deals)
    refund_count = len(refund_deals)

    closed_revenue = closed_deals['Цена'].sum()
    refund_amount = refund_deals['Цена'].sum()

    refund_percent = (refund_count / total_deals * 100) if total_deals > 0 else 0

    console.print(TEXTS['gen_stat'])
    console.print(TEXTS['total_deals'].format(total_deals))
    console.print(TEXTS['total_rev'].format(total_revenue, currency))
    console.print(TEXTS['avg_check'].format(avg_check, currency))

    console.print(TEXTS['closed_deals'])
    console.print(TEXTS['count'].format(closed_count))
    console.print(TEXTS['sum'].format(closed_revenue, currency))

    console.print(TEXTS['refunds'])
    console.print(TEXTS['ref_count'].format(refund_count))
    console.print(TEXTS['ref_sum'].format(refund_amount, currency))
    console.print(TEXTS['ref_percent'].format(refund_percent))
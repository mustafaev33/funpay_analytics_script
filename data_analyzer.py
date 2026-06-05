import pandas as pd
from datetime_analyzer import analyze_dates
from visual import visual_data

print("Loading data from my_sales.csv")
df = pd.read_csv("my_sales.csv")

currency = df['Валюта'].mode()[0] if 'Валюта' in df.columns else '₽'
print(f"\nRecords uploaded: {len(df)}")
print("\nFINANCIAL SUMMARY:")

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

print(f"\nGeneral statistics:")
print(f"Total deals: {total_deals}")
print(f"Total revenue: {total_revenue:.2f} {currency}")
print(f"Average check: {avg_check:.2f} {currency}")

print(f"\nClosed deals:")
print(f"Count: {closed_count}")
print(f"Sum: {closed_revenue:.2f} {currency}")

print(f"\nRefunds:")
print(f"Count: {refund_count}")
print(f"Sum: {refund_amount:.2f} {currency}")
print(f"Return percentage: {refund_percent:.1f}%")

analyze_dates(df, currency)
visual_data(df, currency)
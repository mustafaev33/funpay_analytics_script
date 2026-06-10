import matplotlib.pyplot as plt
import pandas as pd
from dateparser import parse
from __main__ import TEXTS

def visual_data(df, currency):
    df['Цена'] = pd.to_numeric(df['Цена'], errors='coerce')
    dates = df['Дата'].apply(lambda x: parse(x, languages=['ru']))
    monthly = df.groupby(dates.dt.to_period('M'))['Цена'].sum()

    plt.style.use('seaborn-v0_8')

    plt.figure(figsize=(10, 5))
    plt.plot(monthly.index.astype(str), monthly.values, marker='o', linewidth=2, color='#000000')
    plt.title(TEXTS['revenue_visual'].format(currency), fontsize=14, fontweight='bold')
    plt.xlabel('Месяц', fontsize=11)
    plt.ylabel(f'Выручка ({currency})', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.figure(figsize=(10, 5))
    plt.bar(monthly.index.astype(str), monthly.values, width=0.7, color='#000000', edgecolor="#565656")
    plt.title(TEXTS['revenue_visual'].format(currency), fontsize=14, fontweight='bold')
    plt.xlabel('Месяц', fontsize=11)
    plt.ylabel(f'Выручка ({currency})', fontsize=11)
    plt.grid(True, axis='y', alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.figure(figsize=(8, 6))
    status_cnt = df['Статус'].value_counts()
    colors = ["#275E00", "#FF0000", "#ff2200", "#4d1e04"]
    plt.pie(
        status_cnt.values, 
        labels=status_cnt.index, 
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'fontsize': 11}
    )
    plt.title('Succesful deals percentage', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
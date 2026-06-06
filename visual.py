import matplotlib.pyplot as plt
import pandas as pd
from dateparser import parse
from lang_ru import TEXTS
from lang_en import TEXTS

def visual_data(df, currency):

    dates = df['Дата'].apply(lambda x: parse(x, languages=['ru']))
    monthly = df.groupby(dates.dt.to_period('M'))['Цена'].sum()

    plt.style.use('grayscale')

    plt.figure()
    plt.plot(monthly.index.astype(str), monthly.values, marker='o')
    plt.title(TEXTS['revenue_visual'].format(currency))

    plt.figure()
    plt.bar(monthly.index.astype(str), monthly.values, width=0.7)
    plt.title(TEXTS['revenue_visual'].format(currency))

    plt.figure()
    status_cnt = df['Статус'].value_counts()
    plt.pie(status_cnt.values, labels=status_cnt.index, autopct='%1.1f%%',startangle=90)
    plt.title('Succesful deals percentage')
    plt.show()
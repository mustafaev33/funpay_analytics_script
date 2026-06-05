import matplotlib.pyplot as plt
import pandas as pd
from dateparser import parse
from lang_ru import TEXTS
from lang_en import TEXTS

def visual_data(df, currency):
    dates = df['Дата'].apply(lambda x: parse(x, languages=['ru']))
    monthly = df.groupby(dates.dt.to_period('M'))['Цена'].sum()

    plt.plot(monthly.index.astype(str), monthly.values, marker='o')
    plt.title(TEXTS['revenue_visual'].format(currency))
    plt.show()
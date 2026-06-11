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

def save_as_pdf(df, filename):
    from matplotlib.backends.backend_pdf import PdfPages
    rows_per_page = 25
    total_rows = len(df)
    total_pages = (total_rows // rows_per_page) + 1
    
    with PdfPages(filename) as pdf:
        for page_num in range(total_pages):

            start_idx = page_num * rows_per_page
            end_idx = start_idx + rows_per_page
            page_df = df.iloc[start_idx:end_idx]
            
            fig, ax = plt.subplots(figsize=(14, 8))
            ax.axis('tight')
            ax.axis('off')
            
            table = ax.table(
                cellText=page_df.values, 
                colLabels=page_df.columns, 
                cellLoc='center', 
                loc='center'
            )
            
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1.2, 1.5)
            
            plt.title(f"FunPay Sales Report (Страница {page_num + 1} из {total_pages})", 
                     fontsize=14, fontweight='bold', pad=20)
            
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
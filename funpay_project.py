import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from auto_cookie import get_auto_cookies
from rich.console import Console


console = Console()

lang_input = console.input("[bold #10e8a0]Выберите язык / Choose language (ru/en): [/bold #10e8a0]").strip().lower()
lang = 'ru' if lang_input == 'ru' else 'en'
if lang == 'ru':
    from lang_ru import TEXTS
else:
    from lang_en import TEXTS

console.print(TEXTS['welcome'])

default_url = "https://funpay.com/orders/trade"
url_input = console.input(TEXTS['url_input'].format(default_url)).strip()
url = url_input if url_input else default_url

console.print(f"\n{TEXTS['cookie_warn']}")
console.print(TEXTS['cookie_choice'])
choice = console.input(TEXTS['enter_choice'])
cookie = ""

if choice == '1':
    cookie = get_auto_cookies()
elif choice == '2':
    console.print(TEXTS['manual'])
    cookie = console.input(TEXTS['enter_cookie']).strip()
else:
    console.print(TEXTS['wrong_choice'])
    exit()

if len(cookie) <= 20:
    console.print(f"\n{TEXTS['fatal_cookie']}")
    exit()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": cookie
}

console.print(TEXTS['connecting'])
response = requests.get(url, headers=headers)

if response.status_code == 200:
    console.print(TEXTS['success'])
    soup = bs(response.text, "html.parser")
    items = soup.find_all("a", class_= "tc-item")
    console.print(TEXTS['found'].format(len(items)))

    data = []
    for item in items:
        unit_tag = item.find('span', class_='unit')
        currency = unit_tag.text.strip() if unit_tag else '₽'
        date = item.find('div', class_='tc-date-time').text.strip()
        order = item.find('div', class_='tc-order').text.strip()
        desc = item.find('div', class_='order-desc').text.strip()
        status = item.find('div', class_='tc-status').text.strip()
        price = item.find('div', class_='tc-price').text.strip().replace(currency, '').strip()
    
        data.append({
            'Дата': date,
            'Заказ': order,
            'Товар': desc,
            'Статус': status,
            'Цена': price,
            'Валюта': currency            
        })
    df = pd.DataFrame(data)

    console.print(TEXTS['collected'])
    console.print(df)

    save = console.input(TEXTS['save_choice']).strip().lower()
    if save in ["y", "н", "yes", "да", "д"]:
        try:

            old_df = pd.read_csv("my_sales.csv")
            console.print(TEXTS['found_old_file'].format(len(old_df)))
            update_df = pd.concat([old_df, df], ignore_index=True)
            update_df = update_df.drop_duplicates(subset=['Заказ'], keep='first')
            new_notes = len(update_df) - len(old_df)
            update_df.to_csv("my_sales.csv", index=False, encoding="utf-8-sig")
            console.print(TEXTS['success_update'].format(new_notes))
            console.print(TEXTS['total_notes'].format(len(update_df)))

        except FileNotFoundError:
            df.to_csv("my_sales.csv", index=False, encoding="utf-8-sig")
            console.print(TEXTS['saved'])
    else:
        console.print(TEXTS['success_no_save'])
else:
    console.print(TEXTS['error_conn'].format(response.status_code))

if len(df) > 0:
    run_analytics = console.input(TEXTS['run_analytics']).strip().lower()
    if run_analytics in ["y", "н", "yes", "да", "д"]:
        import data_analyzer
        from datetime_analyzer import analyze_dates 
        data_analyzer
        analyze_dates(df, currency)

    run_reviews = console.input(TEXTS['run_reviews']).strip().lower()
    if run_reviews in ["y", "н", "yes", "да", "д"]:
        from reviews_analyzer import check_reviews

        url_rev_input = console.input(TEXTS['enter_prof_url']).strip()
        profile_url = url_rev_input if url_rev_input else None
        if profile_url is None or len(profile_url) < 15:
            console.print(TEXTS['rev_error'])
        else:
            check_reviews(profile_url, headers, TEXTS)

    run_charts = console.input(TEXTS['run_charts']).strip().lower()
    if run_charts in ["y", "н", "yes", "да", "д"]:
        from visual import visual_data
        visual_data(df, currency)
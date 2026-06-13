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

import os

csv_exists = os.path.exists("my_sales.csv")
xlsx_exists = os.path.exists("my_sales.xlsx")

skip_parsing = False

if csv_exists or xlsx_exists:
    if xlsx_exists:
        found_file = "my_sales.xlsx"
    else:
        found_file = "my_sales.csv"

    console.print(TEXTS['found_f'].format(found_file))
    console.print(TEXTS['f_choice'])
    file_choice = console.input(TEXTS['enter_f_choice']).strip().lower()

    if file_choice in ["1", "аналитика", "analytics"]:
        if xlsx_exists:
            df = pd.read_excel("my_sales.xlsx", engine='openpyxl')
        else:
            df = pd.read_csv("my_sales.csv", encoding="utf-8-sig")

        currency = df['Валюта'].mode()[0] if 'Валюта' in df.columns else '₽'

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie": ""
        }

        console.print(TEXTS['loaded_from_file'].format(len(df)))
        skip_parsing = True

if not skip_parsing:
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
            console.print(TEXTS['save_format'])
            format_choice = console.input(TEXTS['enter_format']).strip().lower()

            try:

                old_df = pd.read_csv("my_sales.csv")
                console.print(TEXTS['found_old_file'].format(len(old_df)))
                update_df = pd.concat([old_df, df], ignore_index=True)
                update_df = update_df.drop_duplicates(subset=['Заказ'], keep='first')
                new_notes = len(update_df) - len(old_df)
            except FileNotFoundError:
                update_df = df
                new_notes = len(df)

            if format_choice in ["1", "csv"]:
                update_df.to_csv("my_sales.csv", index=False, encoding="utf-8-sig")
                console.print(TEXTS['saved'].format(new_notes, len(update_df)))
            elif format_choice in ["2", "excel", "xlsx"]:
                import openpyxl
                update_df.to_excel("my_sales.xlsx", index=False, engine='openpyxl')
                console.print(TEXTS['saved_excel'].format(new_notes, len(update_df)))
            elif format_choice in ["3", "pdf"]:
                from visual import save_as_pdf
                save_as_pdf(update_df, "my_sales.pdf")
                console.print(TEXTS['saved_pdf'].format(new_notes, len(update_df)))
            else:
                update_df.to_csv("my_sales.csv", index=False, encoding="utf-8-sig")
                console.print(TEXTS['saved'].format(new_notes, len(update_df)))
        else:
            console.print(TEXTS['success_no_save'])
    else:
        console.print(TEXTS['error_conn'].format(response.status_code))

if len(df) > 0:
    run_analytics = console.input(TEXTS['run_analytics']).strip().lower()
    if run_analytics in ["y", "н", "yes", "да", "д"]:
        from data_analyzer import run_data_analytics
        from datetime_analyzer import analyze_dates 
        run_data_analytics()
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

    parse_lot = console.input(TEXTS['lot_choice']).strip().lower()
    if parse_lot in ["y", "н", "yes", "да", "д"]:
        from funpay_discrb_searcher import parse_lot_info, display_lot_info
        
        lot_url = console.input(TEXTS['enter_lot_url']).strip()
        
        if not lot_url:
            console.print(TEXTS['url_required'])
        else:
            lot_data = parse_lot_info(lot_url, headers, TEXTS)
            display_lot_info(lot_data, TEXTS)

    run_charts = console.input(TEXTS['run_charts']).strip().lower()
    if run_charts in ["y", "н", "yes", "да", "д"]:
        from visual import visual_data
        visual_data(df, currency)
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from auto_cookie import get_auto_cookies

lang_input = input("Выберите язык / Choose language (ru/en): ").strip().lower()
lang = 'ru' if lang_input == 'ru' else 'en'
if lang == 'ru':
    from lang_ru import TEXTS
else:
    from lang_en import TEXTS

print(TEXTS['welcome'])

default_url = "https://funpay.com/orders/trade"
url_input = input(TEXTS['url_input'].format(default_url)).strip()
url = url_input if url_input else default_url

print(f"\n{TEXTS['cookie_warn']}")
print(TEXTS['cookie_choice'])
choice = input(TEXTS['enter_choice'])
cookie = ""

if choice == '1':
    cookie = get_auto_cookies()
elif choice == '2':
    print(TEXTS['manual'])
    cookie = input(TEXTS['enter_cookie']).strip()
else:
    print(TEXTS['wrong_choice'])
    exit()

if len(cookie) <= 20:
    print(f"\n{TEXTS['fatal_cookie']}")
    exit()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": cookie
}

print(TEXTS['connecting'])
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(TEXTS['success'])
    soup = bs(response.text, "html.parser")
    items = soup.find_all("a", class_= "tc-item")
    print(TEXTS['found'].format(len(items)))

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

    print(TEXTS['collected'])
    print(df.head(10))

    save = input(TEXTS['save_choice']).strip().lower()
    if save in ["y", "н", "yes", "да", "д"]:
        try:

            old_df = pd.read_csv("my_sales.csv")
            print(TEXTS['found_old_file'].format(len(old_df)))
            update_df = pd.concat([old_df, df], ignore_index=True)
            update_df = update_df.drop_duplicates(subset=['Заказ'], keep='first')
            new_notes = len(update_df) - len(old_df)
            update_df.to_csv("my_sales.csv", index=False, encoding="utf-8-sig")
            print(TEXTS['success_update'].format(new_notes))
            print(TEXTS['total_notes'].format(len(update_df)))

        except FileNotFound:
            df.to_csv("my_sales.csv", index=False, encoding="utf-8-sig")
            print(TEXTS['saved'])
    else:
        print(TEXTS['success_no_save'])
else:
    print(TEXTS['error_conn'].format(response.status_code))
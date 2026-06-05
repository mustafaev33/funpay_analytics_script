import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from auto_cookie import get_auto_cookies

print("Welcome to FunPay-data collector")

default_url = "https://funpay.com/orders/trade"
url_input = input(f"Enter your sales-page URL (or only push Enter to set default URL: '{default_url}'): ").strip()
url = url_input if url_input else default_url

print("\nWARNING: to collect your data you must enter your cookies")
print("You can choose: ")
print("1.Collect your cookies in auto-mode")
print("2.Enter your cookies manually")
choice = input("Enter 1 for auto-mode or 2 for enter your cookies manually: ")
cookie = ""

if choice == '1':
    cookie = get_auto_cookies()
elif choice == '2':
    print("How?: F12 -> Network -> F5 -> find: funpay.com - trade.html (right click) -> Copy as cURL -> Copy your 'Cookie: '")
    cookie = input("Enter your cookies: ").strip()
else:
    print("Incorrect choice. Disconnecting")
    exit()

if len(cookie) <= 20:
    print("\nFatal error: you aren't enter your cookies. Disconnecting")
    exit()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": cookie
}

print("Try to connect to FunPay")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Succesful connection")
    soup = bs(response.text, "html.parser")
    items = soup.find_all("a", class_= "tc-item")
    print(f"Found {len(items)} sales")

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

    print("Collected data: ")
    print(df.head(10))

    save = input("Do you want to save data to csv-file? Enter y/yes - if yes or other symbol - if no: ").strip().lower()
    if save in ["y", "н", "yes", "да", "д"]:
        try:

            old_df = pd.read_csv("my_sales.csv")
            print(f"Found data-file with {len(old_df)} data-notes. Updating, please wait")
            update_df = pd.concat([old_df, df], ignore_index=True)
            update_df = update_df.drop_duplicates(subset=['Заказ'], keep='first')
            new_notes = len(update_df) - len(old_df)
            update_df.to_csv("my_sales.csv", index=False, encoding="utf-8-sig")
            print(f"Succesful updating! Add {new_notes} new notes")
            print(f"Notes in new data-file: {len(update_df)}")

        except FileNotFound:
            df.to_csv("my_sales.csv", index=False, encoding="utf-8-sig")
            print("Succesful create csv-data file")
    else:
        print("Succesfully")
else:
    print(f"Connection error. Status code: {response.status_code}")
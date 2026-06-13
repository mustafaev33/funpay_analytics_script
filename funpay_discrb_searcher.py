from bs4 import BeautifulSoup as bs
import requests
from rich.console import Console
from __main__ import TEXTS

console = Console()

def parse_lot_info(url, headers, TEXTS):

    try:
        console.print(TEXTS['lot_load'])
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            console.print(TEXTS['prof_error'].format(response.status_code))
            return None
        
        soup = bs(response.text, "html.parser")
        
        title_tag = soup.find("h1", class_="lot-title")
        title = title_tag.text.strip() if title_tag else TEXTS['not_found']
        
        seller_tag = soup.find("a", class_="lot-seller")
        seller = seller_tag.text.strip() if seller_tag else TEXTS['not_found']
        
        params = {}
        param_blocks = soup.find_all("div", class_="param-item")
        for block in param_blocks:
            h5_tag = block.find("h5")
            value_div = block.find("div")
            if h5_tag and value_div:
                param_name = h5_tag.text.strip()
                param_value = value_div.text.strip()
                params[param_name] = param_value
        
        description = TEXTS['no_desc']
        for block in param_blocks:
            h5_tag = block.find("h5")
            if h5_tag and "Подробное описание" in h5_tag.text:
                desc_div = block.find("div")
                if desc_div:
                    description = desc_div.text.strip()
                    break
        
        return {
            "title": title,
            "seller": seller,
            "params": params,
            "description": description
        }
    
    except Exception as e:
        console.print(TEXTS['error_conn'])
        return None


def display_lot_info(lot_data, TEXTS):
    if not lot_data:
        console.print(TEXTS['not_found'])
        return
    
    console.print(TEXTS['lot_title'])
    
    console.print(TEXTS['lot_name'])
    console.print(f"{lot_data['title']}")
    
    console.print(TEXTS['seller'])
    console.print(f"{lot_data['seller']}")
    
    if lot_data['params']:
        console.print(TEXTS['params'])
        for param_name, param_value in lot_data['params'].items():
            if param_name != "Подробное описание":
                console.print(f"[white]{param_name}:[/white] {param_value}")
    
    console.print(TEXTS['desc'])
    console.print(f"[bold cyan]{lot_data['description']}[bold cyan]")
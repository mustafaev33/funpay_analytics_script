import requests
from bs4 import BeautifulSoup as bs
from rich.console import Console
from __main__ import TEXTS

console = Console()

def check_reviews(profile_url, headers, texts):
    response = requests.get(profile_url, headers=headers)
    if response.status_code != 200:
        console.print(TEXTS['prof_error'].format(response.status_code))
        return

    soup = bs(response.text, "html.parser")

    rating_tag = soup.find("span", class_="big")
    rating_text = rating_tag.text.strip() if rating_tag else "Не найден"
    
    review_blocks = soup.find_all("div", class_="review-item-text")[:20]
    all_text = ""
    for block in review_blocks:
        all_text += block.text.lower() + " "

    console.print(TEXTS['rev_title'])
    console.print(TEXTS['rating'].format(rating_text))
    console.print(TEXTS['rev_searched'].format(len(review_blocks)))
    if not review_blocks:
        console.print(TEXTS['rev_error'])
        return
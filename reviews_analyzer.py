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
    if rating_text in ["N/A", "Не найден", ""]:
        console.print(TEXTS['rev_error'])
    else:
        rating_num = float(rating_text)
    if rating_num >= 4.5:
        console.print(TEXTS['green_rating'].format(rating_text))
    elif rating_num >= 3.9:
        console.print(TEXTS['yellow_rating'].format(rating_text))
    else:
        console.print(TEXTS['red_rating'].format(rating_text))

    console.print(TEXTS['rev_searched'].format(len(review_blocks)))
    if not review_blocks:
        console.print(TEXTS['rev_error'])
        return
    
    keywords = TEXTS['good_words'] + TEXTS['bad_words']

    results = []
    for word in keywords:
        count = all_text.count(word)
        if count > 0:
            results.append({"word": word, "count": count})

    results.sort(key=lambda x: x["count"], reverse=True)

    console.print(TEXTS['top_rev_cnt'])
    for item in results:
        rev_word = item["word"]
        rev_num = item["count"]

        if rev_word in TEXTS["good_words"]:
            color = "bold green" 
        elif rev_word in TEXTS["bad_words"]:
            color = "bold red"
        else:
            color = None

        console.print(TEXTS['rev_results'].format(color , item['word'], color, item['count']))
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import re

@dataclass
class Card:
    title: str
    promotion_text: str
    clinic_name: str
    time_to_get: str
    address: str


def parse():
    url = "https://spb.napopravku.ru/"
    urls = [f"{url}aktsii/" if i == 1 else f"{url}aktsii/page-{i}/" for i in range(1, 2)]

    cards = list()
    for u in urls:
        try:
            response = requests.get(u)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            title_elems = soup.select("div.promotion-card__content")
            for e in title_elems:
                title = e.select_one(".h2").text
                promotion_text = e.select_one(".custom-markup").text.replace("Например:", "Например:\n")
                clinic_name = e.select_one(".promotion-contacts__name.promotion-contacts__name--link").text
                time_to_get = e.select_one("div.promotion__tags").text[:-10]
                address = e.select_one(".clinic-address__info").text

                card = Card(title.replace('\n', '').strip(), promotion_text.replace('\n', '').strip(), clinic_name.replace('\n', '').strip(), time_to_get.replace('\n', '').strip(), address.replace('\n', '').strip())
                cards.append(card)

        except Exception as e:
            print(f"An error occurred: {e}")

    return cards
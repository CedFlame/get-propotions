import time

from pyrogram import Client
import json

import parser
import settings


class PEmoji:
    def __init__(self, emoji_id, text):
        self.id = emoji_id
        self.text = text

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text
        }


class Card:
    title: str
    promotion_text: str
    clinic_name: str
    time_to_get: str
    address: str


def read_premium_emoji_from_json(file_path, name: str):
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    if data:
        emoji_data = data.get(name)
        if emoji_data:
            premium_emoji = PEmoji(emoji_data["id"], emoji_data["text"])
            return premium_emoji
    return None


api_id = settings.API_ID
api_hash = settings.API_HASH
phone = settings.PHONE

client = Client(name='me_client', api_id=api_id, api_hash=api_hash, phone_number=phone)

file_path = "premium_emojis.json"


def e(name: str):
    premium_emoji = read_premium_emoji_from_json(file_path, name)
    return premium_emoji.text


def message(data: Card):
    parts = list()
    replaced_parts = list()
    parts.append(data.title)
    parts.append(data.promotion_text)
    for i in parts:
        i = i.replace("%", "//percent//")
        i = i.replace("$", "//dollar//")
        i = i.replace("+", "//plus//")
        i = i.replace("=", "//equals//")
        i = i.replace("1", "//one//")
        i = i.replace("2", "//two//")
        i = i.replace("3", "//three//")
        i = i.replace("4", "//four//")
        i = i.replace("5", "//five//")
        i = i.replace("6", "//six//")
        i = i.replace("7", "//seven//")
        i = i.replace("8", "//eight//")
        i = i.replace("9", "//nine//")
        i = i.replace("0", "//zero//")

        replaced_parts.append(i)
    replaced_parts.append(data.clinic_name)
    replaced_parts.append(data.time_to_get)
    replaced_parts.append(data.address)
    return ((f"<b>{replaced_parts[0]}</b>" + "\n" * 2 +
             e("local") + f"{replaced_parts[2]}" + "\n" * 2 +
             f"<b>{replaced_parts[1]}</b>" + "\n" * 2 +
             f"<b>Адрес: {replaced_parts[4]}</b>" + "\n" * 2 +
             e("time") + f"Акция действует {replaced_parts[3]}" + "\n" * 2 +
             e("nav") + "<a href=\"https://t.me/spb_medical/4\">Навигация по разделам с услугами</a>"
             ).replace("//percent//", e("%"))
            .replace("//dollar//", e("$"))
            .replace("//plus//", e("+"))
            .replace("//equals//", e("="))
            .replace("//one//", e("1"))
            .replace("//two//", e("2"))
            .replace("//three//", e("3"))
            .replace("//four//", e("4"))
            .replace("//five//", e("5"))
            .replace("//six//", e("6"))
            .replace("//seven//", e("7"))
            .replace("//eight//", e("8"))
            .replace("//nine//", e("9"))
            .replace("//zero//", e("0")))


data = parser.parse()

client.start()
for i in data:
    client.send_message('me', message(i), disable_web_page_preview=True)
    time.sleep(1)  # Задержка в 1 секунду

client.stop()

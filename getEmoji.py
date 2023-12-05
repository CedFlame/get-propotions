from pyrogram import Client
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
import json

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


api_id = settings.API_ID
api_hash = settings.API_HASH
phone = settings.PHONE

client = Client(name='me_client', api_id=api_id, api_hash=api_hash, phone_number=phone)

premium_emojis = dict()
emoji_counter = 1


def emoji(client: Client, message: Message):

    global emoji_counter

    if message.from_user.is_self and message.entities:
        custom_emoji_id = message.entities[0].custom_emoji_id
        emoji_text = f"<emoji id={custom_emoji_id}>{message.text}</emoji>"
        premium_emoji = PEmoji(custom_emoji_id, emoji_text)
        premium_emojis[str(emoji_counter)] = premium_emoji.to_dict()
        emoji_counter += 1


try:
    client.add_handler(MessageHandler(emoji))
    client.run()
finally:
    with open("premium_emojis.json", "w", encoding="utf-8") as json_file:
        json.dump(premium_emojis, json_file, ensure_ascii=False, indent=2)

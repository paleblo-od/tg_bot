import json
import os

from dotenv import load_dotenv

load_dotenv('example.env')


def load(target):
    with open('utils/misc/dialog.json', 'r', encoding="utf-8") as data:
        data = json.load(data)[target]
        return data


class ProccesDirector():

    def dialog(self, target):
        data = load(target)
        for values, keys in data.items():
            setattr(self, values, keys)

    def get (self, *target):
        level, key = target
        menu = getattr(self, "structure")[str(level)]
        key = getattr(self, menu)[key]
        return key

pd = ProccesDirector()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
DATABASE = str(os.getenv("DATABASE"))
DIALOG = pd
admin = os.getenv("ADMIN_ID")


SHOP_API_TOKEN = os.getenv("SHOP_API_TOKEN")
SHOP_ID = os.getenv("SHOP_ID")

ip = os.getenv("IP")
POSTGRES_URL = F'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'

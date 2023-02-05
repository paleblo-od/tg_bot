
import json

import asyncio
from yookassa import Configuration, Payment


from data import config



Configuration.account_id = config.SHOP_ID
Configuration.secret_key = config.SHOP_API_TOKEN




## from utils.db_api.qiwi import add_payment
# wallet = pyqiwi.Wallet(token=QIWI_TOKEN, number=WALLET_QIWI)
# from pyqiwi import generate_form_link


class NotEnoughMoney:
    pass


class NoPaymentFound(Exception):
    pass


class Payed:

    def __init__(self, amount):
        self.payment = None
        self.message = None
        self.url = None
        self.id = None
        self.amount = amount

    async def create(self):
        with open('utils/misc/payment.json') as data:
            data = json.load(data)
            data["amount"]["value"] = self.amount
            payment = Payment.create(data)
        payment_data = json.loads(payment.json())
        self.id = payment_data['id']
        self.url = (payment_data['confirmation'])['confirmation_url']

    async def start_check(self, message):
        self.message= message
        self.payment = json.loads((Payment.find_one(self.id)).json())
        while self.payment['status'] != 'succeeded':
            self.payment = json.loads((Payment.find_one(self.id)).json())
            await asyncio.sleep(5)
        print(self.payment)
        return self.id

    @property
    def link(self):
        return self.url

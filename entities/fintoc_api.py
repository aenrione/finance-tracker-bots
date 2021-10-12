import os
from dotenv import load_dotenv
from fintoc import Fintoc


load_dotenv()

FINTOC_LINK = os.getenv("FINTOC_LINK")
FINTOC_API_SECRET = os.getenv("FINTOC_API_SECRET")


class FintocApi():
    def __init__(self, name="Fintoc"):
        self.name = name
        self.client = Fintoc(FINTOC_API_SECRET)
        self.link_info = self.client.links.get(FINTOC_LINK)

    def get_current_balance(self):
        balance = 0
        insitution_name = self.link_info.serialize()['institution']['name']
        accounts = self.link_info.accounts.all(lazy=False)
        for account in accounts:
            parsed_info = account.serialize()
            balance += float(parsed_info['balance']['current'])

        output = f"\n ${balance:,.0f} in {insitution_name} ({self.name})"
        return balance, output

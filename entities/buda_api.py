import os
from dotenv import load_dotenv
import surbtc
from parameters import BUDA_CRYPTO_LIST, BUDA_USEFULL_INDEX


load_dotenv()

BUDA_API_KEY = os.getenv("BUDA_API_KEY")
BUDA_API_SECRET = os.getenv("BUDA_API_SECRET")


class BudaApi():
    def __init__(self, name="Buda"):
        self.name = name
        self.client = surbtc.Client(BUDA_API_KEY, BUDA_API_SECRET)

    def get_current_balance(self):
        balance = 0
        output = ""

        for crypto in BUDA_CRYPTO_LIST:
            conversion_rate = self.client \
                .getTicker(f"{crypto}-CLP")['last_price'][BUDA_USEFULL_INDEX]
            crypto_balance = self.client \
                .getBalance(crypto)["amount"][BUDA_USEFULL_INDEX]
            tmp_balance = float(conversion_rate)*float(crypto_balance)
            balance += tmp_balance
            output += f"\n ${tmp_balance:,.0f} in {crypto} ({self.name})"

        return balance, output

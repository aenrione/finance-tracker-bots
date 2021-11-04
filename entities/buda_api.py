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
            market = self.client.getMarket(f"{crypto}-CLP")
            orders = market.getTradedOrders()
            invested = 0
            for order in orders:
                invested += self.__get_order_invested_value(order)
            conversion_rate = self.client \
                .getTicker(f"{crypto}-CLP")['last_price'][BUDA_USEFULL_INDEX]
            crypto_balance = self.client \
                .getBalance(crypto)["amount"][BUDA_USEFULL_INDEX]
            tmp_balance = float(conversion_rate)*float(crypto_balance)
            balance += tmp_balance
            i_s = f"(of ${invested:,.0f} CLP)"
            output += f"\n ${tmp_balance:,.0f} {i_s} in {crypto} ({self.name})"

        return balance, output

    def __get_order_invested_value(self, order):
        tmp_exchanged = float(order["total_exchanged"][BUDA_USEFULL_INDEX])
        if order["type"] == "Ask":
            tmp_exchanged = -tmp_exchanged
        return tmp_exchanged

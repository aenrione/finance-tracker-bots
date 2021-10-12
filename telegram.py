import os
from dotenv import load_dotenv
import surbtc
from fintoc import Fintoc
import requests
import json
import telebot


# Load Env Variables
load_dotenv()

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
FINTOC_LINK = os.getenv("FINTOC_LINK")
FINTOC_API_SECRET = os.getenv("FINTOC_API_SECRET")
BUDA_API_KEY = os.getenv("BUDA_API_KEY")
BUDA_API_SECRET = os.getenv("BUDA_API_SECRET")
FINTUAL_URL = "https://fintual.cl/api"
FINTUAL_EMAIL = os.getenv("FINTUAL_EMAIL")
FINTUAL_PASSWORD = os.getenv("FINTUAL_PASSWORD")

# Load TelegramBot
bot = telebot.TeleBot(TELEGRAM_API_KEY, parse_mode=None)


@bot.message_handler(commands=['get_balance'])
def calculate_balance(message):
    bot.send_message(message.chat.id, "Calculando...")
    balance_message = 'Wallet:\n'
    # Fintoc Info
    fintoc_client = Fintoc(FINTOC_API_SECRET)
    fintoc_info = fintoc_client.links.get(FINTOC_LINK)
    fintoc_institution = fintoc_info.serialize()['institution']['name']
    fintoc_account = fintoc_info.accounts.all(lazy=False)[0].serialize()
    fintoc_balance = (float(fintoc_account['balance']['current']))

    # Fintual Info
    payload = {'user': {'email': FINTUAL_EMAIL, 'password': FINTUAL_PASSWORD}}
    headers = {'Content-type': 'application/json'}
    r = requests.post(FINTUAL_URL + '/access_tokens',
                      data=json.dumps(payload),
                      headers=headers)
    if r.ok:
        access_token = r.json()['data']['attributes']['token']
        goals_request = requests.get(FINTUAL_URL+'/goals',
                                     params={
                                        'user_email': FINTUAL_EMAIL,
                                        'user_token': access_token})
        fintual_account = goals_request.json()['data'][0]
        fintual_account_name = fintual_account['attributes']['name']
        fintual_balance = (float(
            fintual_account['attributes']['nav']))

    # Buda Info
    surbtc_client = surbtc.Client(BUDA_API_KEY, BUDA_API_SECRET)

    btc_clp_price = surbtc_client.getTicker('BTC-CLP')['last_price'][0]
    eth_clp_price = surbtc_client.getTicker('ETH-CLP')['last_price'][0]
    btc_balance = surbtc_client.getBalance("BTC")["amount"][0]
    eth_balance = surbtc_client.getBalance("ETH")["amount"][0]
    btc_to_clp = (float(btc_clp_price)*float(btc_balance))
    eth_to_clp = (float(eth_clp_price)*float(eth_balance))

    # Add to Message
    balance_message += f"\n ${fintoc_balance:,.0f} in " + \
        f"{fintoc_institution} (Fintoc)"
    balance_message += f"\n ${fintual_balance:,.0f} in " + \
        f"{fintual_account_name} (Fintual)"
    balance_message += f"\n ${btc_to_clp:,.0f} in BTC (Buda)"
    balance_message += f"\n ${eth_to_clp:,.0f} in ETH (Buda)"

    total = fintoc_balance + fintual_balance +\
        btc_to_clp + eth_to_clp

    balance_message += f"\n\n ${total:,.0f} in total"

    bot.send_message(message.chat.id, balance_message)


bot.infinity_polling()

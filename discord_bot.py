import discord
import os
from dotenv import load_dotenv
from entities.fintual_api import FintualApi
from entities.fintoc_api import FintocApi
from entities.buda_api import BudaApi
from parameters import NUM_BALANCE_IDX, STR_BALANCE_IDX
from requests import ConnectionError
from fintoc.errors import InvalidRequestError, AuthenticationError

# Load Env Variables
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

client = discord.Client()


@client.event
async def on_ready():
    print(f"{client.user} logged in now!")


@client.event
async def on_message(message):
    if message.content.startswith("/get_balance"):
        await message.channel.send("Calculando...")
        try:
            balance_message = 'Wallet:\n'

            fintoc_balance = FintocApi().get_current_balance()
            buda_balance = BudaApi().get_current_balance()
            fintual_balance = FintualApi().get_current_balance()

            balance_message += fintoc_balance[STR_BALANCE_IDX] + \
                buda_balance[STR_BALANCE_IDX] + \
                fintual_balance[STR_BALANCE_IDX]

            total = fintoc_balance[NUM_BALANCE_IDX] + \
                buda_balance[NUM_BALANCE_IDX] + \
                fintual_balance[NUM_BALANCE_IDX]

            balance_message += f"\n\n ${total:,.0f} in total"
        except ConnectionError as err:
            balance_message = f"Buda Error: \n{err}"
        except (InvalidRequestError, AuthenticationError) as err:
            balance_message = f"Fintoc Error: \n{err}"
        except ValueError as err:
            balance_message = f"Fintual Error: \n{err}"

        await message.channel.send(balance_message)

client.run(DISCORD_BOT_TOKEN)

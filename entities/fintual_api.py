import os
from dotenv import load_dotenv
import json
import requests
from parameters import FINTUAL_URL

load_dotenv()

FINTUAL_EMAIL = os.getenv("FINTUAL_EMAIL")
FINTUAL_PASSWORD = os.getenv("FINTUAL_PASSWORD")


class FintualApi():
    def __init__(self, name="Fintual"):
        self.name = name
        self.token = self.__get_access_token()

    def get_current_balance(self):
        if self.token is None:
            return

        balance = 0
        output = ""
        goals_request = requests.get(FINTUAL_URL+'/goals',
                                     params={
                                        'user_email': FINTUAL_EMAIL,
                                        'user_token': self.token})
        goals = goals_request.json()['data']

        for goal in goals:
            goal_name = goal['attributes']['name']
            goal_balance = float(goal['attributes']['nav'])
            balance += goal_balance
            output += f"\n ${goal_balance:,.0f} in {goal_name} ({self.name})"

        return balance, output

    def __get_access_token(self):
        payload = {
                'user': {'email': FINTUAL_EMAIL, 'password': FINTUAL_PASSWORD}
                }
        headers = {'Content-type': 'application/json'}
        r = requests.post(FINTUAL_URL + '/access_tokens',
                          data=json.dumps(payload),
                          headers=headers)
        if r.ok:
            return r.json()['data']['attributes']['token']
        else:
            raise ValueError('Invalid Fintual credentials.')

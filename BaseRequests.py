import requests
import json
from keys import keys
session = requests.Session()
base_url = f"{keys.OANDA_URL}/"

#this class contains all the http methods required for the bot
class BaseRequests():

    def get (self, endpoint, params, headers):
        response = session.get(base_url + endpoint, params=params, headers=headers)
        return response

    def post (self, endpoint, data, headers):
        response = session.post(base_url + endpoint, json=data, headers=headers)
        return response

    def put (self, endpoint, data, headers):
        response = session.put(base_url + endpoint, json=data, headers=headers)
        return response
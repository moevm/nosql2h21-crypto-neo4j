import requests
import time
import json


class API:
    def __init__(self):
        self.url = "http://api.coincap.io/v2"
        self.headers = {"Authorization": "Bearer 88d0c750-1096-4c6d-9352-932cd40a0500"}

    def get_currencies(self):
        response = self.get("/assets")
        return response

    def get_currency_by_id(self, id):
        response = self.get(f"/assets/{id}")
        return response

    def get(self, query):
        url = self.url + query

        response = requests.request("GET", url, headers=self.headers)
        # Обработка 429 ошибки
        times = 0
        while response.status_code != 200 or times < 3:
            time.sleep(0.5)
            response = requests.request("GET", url, headers=self.headers)
            times += 1

        if response.status_code != 200:
            return {}

        return json.loads(response.text)

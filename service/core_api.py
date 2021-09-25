import logging
import requests
import logging


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)


class CoreAPI:
    def __init__(self, module_name, description, type):
        self.host = 'https://api-digit.siberian-hub.ru/v1/'
        self.module_name = module_name
        self.description = description
        self.type = type

    def register_module(self):
        method = 'module/'
        payload = {
            "name": self.module_name,
            "description": self.description,
            "type": self.type
        }
        return self.request(self.host + method, payload)

    def send_data(self, username, value):
        method = f'module/{self.module_name}/send/'
        payload = {
            "username": username,
            "value": value,
        }

        response = self.request(self.host + method, payload)
        logging.info("DATA SENDED")
        return response

    def request(self, url, payload):
        response = requests.post(url, data=payload)
        if response.status_code == 201:
            return response
        logging.error(url)
        logging.error(response.status_code)
        logging.error(response.content.decode())

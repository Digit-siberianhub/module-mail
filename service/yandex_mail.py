import requests
import logging


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)


class YandexMail:
    def __init__(self, domain: str, pdd_token: str):
        self.host = 'https://pddimp.yandex.ru'
        self.domain = domain
        self.headers = {'PddToken': pdd_token}

    def get_count_letters(self, mail) -> dict:
        """
        Получение статистики о письмах
        Поля:
            new: количество писем, полученных после последней проверки почтового ящика,
            unread: количество непрочитанных писем
        """
        query_params = {'domain': self.domain,'login': mail}
        content = self.request('/api2/admin/email/counters', query_params)
        return content.get('counters')

    def email_list(self):
        """Получение всех почтовых ящиков"""
        query_params = {'domain': self.domain}
        content = self.request('/api2/admin/email/list', query_params)
        return self.filter_accounts(content.get("accounts"))      

    def request(self, method: str, params: dict):
        """Запрос в API яндекс почты"""
        url = self.host + method
        response = requests.get(url, headers=self.headers, params=params)
        content = response.json()
        if response.status_code == 200 and content.get('success') == 'ok':
            return content
        logging.error(response.status_code)
        logging.error(response.content)
        return {}

    def filter_accounts(self, accounts: list):
        """Проверка на робота"""
        for acc in accounts:
            if acc['iname'].lower() != "робот":
                yield self.get_valid_email(acc['login'])

    def get_valid_email(self, email):
        """Проверка на почту с правильным доменом"""
        return email.split('@')[0] + f'@{self.domain}'

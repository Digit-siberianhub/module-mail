import requests
import re
import logging


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)


class YandexMail:
    def __init__(self, domain: str, pdd_token: str):
        self.host = 'https://pddimp.yandex.ru'
        self.pdd_token = pdd_token
        self.domain = domain

    def get_count_letters(self, mail) -> dict:
        """
        Получение статистики о письмах
        Поля:
            new: количество писем, полученных после последней проверки почтового ящика,
            unread: количество непрочитанных писем
        """

        url = self.host + '/api2/admin/email/counters'
        headers = {'PddToken': self.pdd_token}
        query_params = {
            'domain': self.domain,
            'login': mail
        }

        response = requests.get(url, headers=headers, params=query_params)
        content = response.json()
        if response.status_code == 200 and content['success'] != 'error':
            return content['counters']
        
        logging.error(response.status_code)
        logging.error(response.content)

    def email_list(self):
        """Получение всех почтовых ящиков"""
        url = self.host + '/api2/admin/email/list'
        headers = {'PddToken': self.pdd_token}
        query_params = {'domain': self.domain}
        response = requests.get(url, headers=headers, params=query_params)
        content = response.json()
        if response.status_code == 200 and content['success'] != 'error':
            return self.filter_accounts(content.get("accounts"))

        logging.error(response.status_code)
        logging.error(response.content)      

    def filter_accounts(self, accounts):
        """Проверка на робота"""
        clean_accs = []
        for acc in accounts:
            if acc['iname'].lower() != "робот":
                clean_accs.append(self.get_valid_email(acc['login']))
        return clean_accs

    def get_valid_email(self, email):
        """Проверка на почту с правильным доменом"""
        domain = re.search("@[\w.-]+", email).group()
        print("EMAIL", email)
        print("DOMAIN", domain)
        print(40*"-")
        if domain.replace('@', '') == self.domain:
            return email
        return re.sub(r"@[\w.]+", '@' + self.domain, email)

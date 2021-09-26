from time import sleep
import logging

from service.yandex_mail import YandexMail
from service.db_api import DBApi
from service.core_api import CoreAPI
import service.credentials as creds


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)

TIME = 300
ym = YandexMail(creds.DOMAIN, creds.PDD_TOKEN)
db = DBApi(creds.DATABASE_URL)
core = CoreAPI(
    'Почта',
    'Модуль для работы с корпоративными почтами',
    'Социальное'
)


def scheduled(wait_for):
    while True:
        logging.info('CHECKING MAILS')
        for email in ym.email_list():
            payload = ym.get_count_letters(email)
            if not payload:
                continue
            logging.info(email + ' ' + str(payload))
            user = db.get_user(email)
            if not user:
                user = db.create_user(email, unread=payload['unread'], new=payload['new'])

            if payload['unread'] != user.unread:
                core.send_data(email, user.unread - payload['unread'])
                db.set_new_counters(user, unread=payload['unread'], new=payload['new'])

        sleep(wait_for)


if __name__ == '__main__':
    logging.info("START MAIL MODULE")
    core.register_module()
    scheduled(TIME)

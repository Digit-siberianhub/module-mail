from time import sleep
import logging

from service.yandex_mail import YandexMail
from service.db_api import DBApi
import service.credentials as creds



logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)

TIME = 5
ym = YandexMail(creds.DOMAIN, creds.PDD_TOKEN)
db = DBApi(creds.DATABASE_URL)


def scheduled(wait_for):
    while True:
        logging.info('CHECKING MAILS')
        for email in ym.email_list():
            payload = ym.get_count_letters(email)
            if payload:
                logging.info(email + ' ' + str(payload))
                user = db.get_user(email)
                if user:
                    if payload['unread'] != user.unread or payload['new'] != user.new:
                        db.set_new_counters(user, unread=payload['unread'], new=payload['new'])
                        # запрос в ядро
                db.create_user(email, unread=payload['unread'], new=payload['new'])
        sleep(wait_for)


if __name__ == '__main__':
    logging.info("START MAIL MODULE")
    # регистрация модуля в ядре
    scheduled(TIME)

import asyncio
from service.yandex_mail import YandexMail
import credentials.yandex as yd_cred
import logging


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)

ym = YandexMail(yd_cred.DOMAIN, yd_cred.PDD_TOKEN)


async def scheduled(wait_for):
    while True:
        logging.info('CHECKING MAILS')
        for email in ym.email_list():
            payload = ym.get_count_letters(email)
            if payload:
                logging.info(payload)
                # запрос в ядро
        await asyncio.sleep(wait_for)


if __name__ == '__main__':
    logging.info("START MAIL MODULE")
    # регистрация модуля в ядре
    asyncio.run(scheduled(5))


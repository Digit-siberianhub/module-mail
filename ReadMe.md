# Модуль для работы с почтой

## Руководство по запуску

1. Для начала нужно получить токен, для работы с API Яндекс 360 -> [инструкция](https://pddimp.yandex.ru/api2/admin/get_token)

2. Склонировать репозиторий
    ```
    git clone git@github.com:Digit-siberianhub/module-mail.git
    ```

3. Перейти в папку модуля
    ```
    cd module-mail
    ```

4. Установить [python3.9](https://www.python.org/downloads/)

5. Установить [pip](https://pip.pypa.io/en/stable/installation/)

6. Установить пакетный менеджер [pipenv](https://webdevblog.ru/pipenv-rukovodstvo-po-novomu-instrumentu-python/)
    ```
    pip install pipenv
    ```

7. В корне создать файл **.env**

8. В файле **.env** прописать переменные окружения
    ```
    DOMAIN_YANDEX='домен_вашей_компании'
    PDD_TOKEN_YANDEX='PDD_токен_администратора_в_Яндекс_360'
    DATABASE_URL='sqlite:///test.db'
    ```

9. Создать виртуальное окружение через pipenv
    ```
    pipenv shell
    ```

10. Установить все необходимые зависимости
    ```
    pipenv install --dev
    ```

11. Запуск модуля
    ```
    python main.py
    ```

# Тестовое задание для компании Радиум
## Скрипт для скачивания содержимого HEAD репозитория
Этот скрипт на Python асинхронно скачивает содержимое HEAD репозитория
https://gitea.radium.group/radium/project-configuration во временную папку.


## Требования
Для использования этого скрипта вам нужно установить Python 3 и все необходимые
библиотеки, которые указаны в файле requirements.txt. Вы можете установить все,
выполнив следующую команду:

```sh
pip install -r requirements.txt
```

## Использование
1. Скачайте скрипт из репозитория:
    ```sh
    git clone https://github.com/mikholand/test_radium.git
    cd radium_test
    ```
2. Запустите скрипт:
    ```sh
    python main.py
    ```

Подождите, пока скрипт скачает содержимое репозитория. Это занимает пару секунд
в зависимости от скорости вашего интернет-соединения.

После завершения работы скрипта вы найдете содержимое HEAD репозитория
во временной папке папке.

## Лицензия
Этот скрипт распространяется на условиях лицензии MIT. 
Подробности смотрите в файле
[LICENSE](https://github.com/mikholand/radium_test/blob/master/LICENSE).

## Контакты
Михно Олег - [Telegram](https://t.me/mikholand) - mikholand@gmail.com

GitHub: [https://github.com/mikholand](https://github.com/mikholand)

LinkedIn: [https://www.linkedin.com/in/mikholand/](https://www.linkedin.com/in/mikholand/)

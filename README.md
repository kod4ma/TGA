# TGA - Telegram Assistant

Telegram Assistant - _заместитель_ и _помощник_ в выполнении рутинных задач при использовании мессенджера. Состоит из основного демона и телеграм-бота для взаимодействия с владельцем аккаунта.

## Установка
Для работы потребуется `TkInter 8.6`. Все остальные пререквизиты внесены в `requirements.txt`

```bash
$ git clone https://github.com/kod4ma/TGA
$ cd TGA
$ sudo apt-get install python3-tk
$ pip install -r requirements.txt
```

## Запуск
Для работы необходимы параметры `api_hash` и `api_id`, взятые с [my.telegram.org](https://my.telegram.org).

TGA также использует ссылку на приватную группу в телеграме для уведомлений (не обязательное поле).

### Пример работы
```bash
$ ./main.py
First time hello! Let's configure your TGA
api_hash: <hex string>
api_id: <integer>
Monitor group invite link: https://t.me/joinchat/IxisqJdw8-1
Great! You can edit your configuration at storage/config.json
Please enter your phone (or bot token): +7XXXXXXXXXX
Please enter the code you received: 12345
Please enter your password:
Logged in successfully as Sauron
[*] TGA is logged in and listening for events...
NewMessage[575086]: <Мой пароль: 3poulakia!> from Phi
NewMessage[575087]: <ой, не тот чат> from Phi
MessageDeleted[575086]: <Мой пароль: 3poulakia!> from Phi
MessageDeleted[575087]: <ой, не тот чат> from Phi
```

## Постановка задачи

Написать программу **TGA** на [Telethon](https://github.com/LonamiWebs/Telethon), включающую в себя три модуля:

* Автоответчик
* Сохранятор
* Чайка-менеджер

## Описание модулей

### Автоответчик

Данный модуль позволяет перевести мессенджер в режим автоответчика, который:

* отвечает людям заранее заготовленными сообщениями из словаря
* имеет чувство юмора

### Сохранятор

Данный модуль позволяет мониторить приходящие сообщения и сохранять удаленные. Пример - кто-то прислал сообщение, а потом удалил его => мы не успели прочитать. С помощью этого модуля можно перехватить сообщение до удаления.

### Чайка-менеджер

Данный модуль выполняет функции неэффективного менеджера, который с юмором напоминает определенным контактам о их задачах. К особым функциям относятся напоминания-многоходовочки.

#!/usr/bin/env python3
"""Telegram Assistant is a Telegram daemon that automates user tasks.

TGA is created for simplifying the process of performing routine job
in Telegram Messenger and also for casting some fancy message magic.
"""

import json
import os
import random
import string
import sqlite3
import telethon
import time
import ast
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from datetime import timedelta


class Application(tk.Frame):
    """Class for working with tkinter."""

    def __init__(self, master=None):
        """Initialize of the main window."""
        super().__init__(master)
        self.master.title("TGA ^_^")
        self.master.minsize(width=600, height=400)
        self.master.columnconfigure(3, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.configuration = {'manage': {}, 'save': {}, 'ansver': {}}
        self.create_widgets()

    def create_widgets(self):
        """Create widgets."""
        self.F = tk.LabelFrame(self.master)
        self.F.grid(sticky='news', columnspan=3, row=0)
        self.F.quit = tk.Button(self.F, text="Применить настройки",
                                command=self.save_config)
        self.F.quit.grid(column=3, row=0)

        self.F.quit = tk.Label(self.F)
        self.F.quit["text"] = ("Выберете и настройте модули которые "
                               + "будут запущены    ")
        self.F.quit.grid(column=0, row=0)

        self.f1 = tk.LabelFrame(self.master)
        self.f1.rowconfigure(8, weight=1)
        self.f1.grid(sticky='nsew', column=0, row=1)
        self.on_manage(first_time=True)

        self.f2 = tk.LabelFrame(self.master, width=1000, height=100)
        self.f2.rowconfigure(5, weight=1)
        self.f2.grid(sticky='nsew', column=1, row=1)
        self.on_saver(first_time=True)

        self.f3 = tk.LabelFrame(self.master)
        self.f3.rowconfigure(5, weight=1)
        self.f3.grid(sticky='nsew', column=2, row=1)
        self.on_auto(first_time=True)

    def off_auto(self):
        """Render an enabled answering machine."""
        print("off_auto")
        self.f3.newb.grid_forget()
        self.f3.com_lab.grid_forget()
        self.f3.combo.grid_forget()
        self.f3.lab.grid_forget()
        self.f3.off_auto = tk.Button(self.f3)
        self.f3.off_auto["text"] = "Отключить автоответчик"
        self.f3.off_auto["command"] = self.on_auto
        self.f3.off_auto.grid(sticky='nsew', column=0, row=0)
        self.f3.off_lab = tk.Label(self.f3, font='Times 15', fg='#247719')
        self.f3.off_lab["text"] = ("Автоответчик будет включен\n в режимe "
                                   + self.f3.combo.get())
        self.f3.off_lab.grid(column=0, row=1)
        self.configuration['ansver']['enabel'] = True
        self.configuration['ansver']['dic'] = self.f3.combo.get()

    def on_auto(self, first_time=False):
        """Render of the choice of the optsy autoresponder."""
        print("on_auto")
        if not first_time:
            self.f3.off_auto.grid_forget()
            self.f3.off_lab.grid_forget()
        self.f3.newb = tk.Button(self.f3)
        self.f3.newb["text"] = "Включить автоответчик"
        self.f3.newb["command"] = self.off_auto
        self.f3.newb.grid(sticky='nsew', column=0, row=0)

        self.f3.com_lab = tk.Label(self.f3)
        self.f3.com_lab["text"] = "Причина включения автоответчика:"
        self.f3.com_lab.grid(column=0, row=2)
        self.f3.combo = ttk.Combobox(self.f3, values=[
                                    "Все бесят",
                                    "Ночное время",
                                    "Важная встреча",
                                    "Экзамен",
                                    "Детокс"])
        self.f3.combo.current(0)
        self.f3.combo.grid(column=0, row=3)

        self.f3.lab = tk.Label(self.f3, font='Times 15', fg='#960018')
        self.f3.lab["text"] = "Aвтоответчик будет выключен"
        self.f3.lab.grid(column=0, row=1)
        self.configuration['ansver'] = {}

    def on_saver(self, first_time=False):
        """Render of the choice of the optsy save machine."""
        print("save_me")
        if not first_time:
            self.f2.off_newb.grid_forget()
            self.f2.lab.grid_forget()
        self.f2.newb = tk.Button(self.f2)
        self.f2.newb["command"] = self.off_saver
        self.f2.newb["text"] = "Включить сохронятор"
        self.f2.newb.grid(column=0, row=0)
        self.f2.lab_m = tk.Label(self.f2)
        self.f2.lab_m["text"] = ("Ссылка на группу для уведомлений\n"
                                 + "(не обязательное поле)")
        self.f2.lab_m.grid(column=0, row=2)
        self.f2.message = tk.StringVar()
        self.f2.message_entry = tk.Entry(self.f2, textvariable=self.f2.message)
        self.f2.message_entry.grid(column=0, row=3)
        self.f2.lab = tk.Label(self.f2, font='Times 15', fg='#960018')
        self.f2.lab["text"] = "Сохранятор будет выключен"
        self.f2.lab.grid(column=0, row=1)
        self.configuration['save'] = {}

    def off_saver(self):
        """Render an enabled save machine."""
        self.f2.newb.grid_forget()
        self.f2.lab.grid_forget()
        self.f2.lab_m.grid_forget()
        self.f2.message_entry.grid_forget()
        self.f2.off_newb = tk.Button(self.f2)
        self.f2.off_newb["command"] = self.on_saver
        self.f2.off_newb["text"] = "Отключить сохронятор"
        self.f2.off_newb.grid(column=0, row=0)
        self.f2.lab = tk.Label(self.f2, font='Times 15', fg='#247719')
        self.f2.lab["text"] = "Сохранятор будет включен"
        self.f2.lab.grid(column=0, row=1)
        self.f2.lab = tk.Label(self.f2, font='Times 15', fg='#247719')
        self.configuration['save']['enabel'] = True
        if self.f2.message.get() == "":
            self.f2.lab["text"] = "Без группы уведомлений"
        else:
            self.f2.lab["text"] = "Адрес группы уведомлений получен"
            self.configuration['save']['group'] = self.f2.message.get()
        self.f2.lab.grid(column=0, row=2)

    def on_manage(self, first_time=False):
        """Render of the choice of the optsy manage machine."""
        print("manage")
        if not first_time:
            self.f1.off_newb.grid_forget()
            self.f1.lab_info.grid_forget()
        self.f1.newb = tk.Button(self.f1)
        self.f1.newb["text"] = "Включить менеджера"
        self.f1.newb["command"] = self.off_manage
        self.f1.newb.grid(sticky='nsew', column=0, row=0)
        self.f1.lab_id = tk.Label(self.f1)
        self.f1.lab_id["text"] = ("Номер исполнителя:")
        self.f1.lab_id.grid(column=0, row=2)
        self.f1.m_id = tk.StringVar()
        self.f1.id_entry = tk.Entry(self.f1, textvariable=self.f1.m_id)
        self.f1.id_entry.grid(column=0, row=3)

        self.f1.lab_task = tk.Label(self.f1)
        self.f1.lab_task["text"] = ("Задача:")
        self.f1.lab_task.grid(column=0, row=4)
        self.f1.m_task = tk.StringVar()
        self.f1.task_entry = tk.Entry(self.f1, textvariable=self.f1.m_task)
        self.f1.task_entry.grid(column=0, row=5)

        self.f1.lab_day = tk.Label(self.f1)
        self.f1.lab_day["text"] = ("Кол-во дней до дедлайна:")
        self.f1.lab_day.grid(column=0, row=6)
        self.f1.m_day = tk.StringVar()
        self.f1.day_entry = tk.Entry(self.f1, textvariable=self.f1.m_day)
        self.f1.day_entry.grid(column=0, row=7)

        self.f1.lab = tk.Label(self.f1, font='Times 15', fg='#960018')
        self.f1.lab["text"] = "Чайка-менеджер будет включен"
        self.f1.lab.grid(column=0, row=1)
        self.configuration['manage'] = {}

    def off_manage(self):
        """Render an enabled manage machine."""
        print("off_manage")

        if self.f1.m_day.get() == "" or self.f1.m_task.get() == "" \
                or self.f1.m_id.get() == "":
            mb.showerror(title="Ошибка",
                         message="Все поляявляются обязательными "
                         + "для начтройки Чайки")
            self.f1.newb.grid_forget()
            self.f1.lab_id.grid_forget()
            self.f1.lab.grid_forget()
            self.f1.id_entry.grid_forget()
            self.f1.lab_task.grid_forget()
            self.f1.task_entry.grid_forget()
            self.f1.lab_day.grid_forget()
            self.f1.day_entry.grid_forget()
            self.on_manage(first_time=True)
            return

        print("1off_manage")
        self.f1.newb.grid_forget()
        self.f1.lab_id.grid_forget()
        self.f1.lab.grid_forget()
        self.f1.id_entry.grid_forget()
        self.f1.lab_task.grid_forget()
        self.f1.task_entry.grid_forget()
        self.f1.lab_day.grid_forget()
        self.f1.day_entry.grid_forget()

        self.f1.off_newb = tk.Button(self.f1)
        self.f1.off_newb["command"] = self.on_manage
        self.f1.off_newb["text"] = "Отключить менеджера"
        self.f1.off_newb.grid(column=0, row=0)

        self.f1.lab = tk.Label(self.f1, font='Times 15', fg='#247719')
        self.f1.lab["text"] = "Чайка-менеджер будет включен"
        self.f1.lab.grid(column=0, row=1)

        self.f1.lab_info = tk.Label(self.f1, font='Times 15', fg='#247719')
        self.f1.lab_info["text"] = ("\n\nЗадача " + self.f1.m_task.get()
                                    + "\nбудет выдана " + self.f1.m_id.get()
                                    + "\nна срок " + self.f1.m_day.get()
                                    + "(в днях)")
        self.f1.lab_info.grid(column=0, row=2)
        self.configuration['manage']['enabel'] = True
        self.configuration['manage']['task'] = self.f1.m_task.get()
        self.configuration['manage']['id'] = self.f1.m_id.get()
        self.configuration['manage']['day'] = self.f1.m_day.get()

    def save_config(self):
        """Output validation function."""
        self.master.destroy()


class TelegramAssistant():
    """A single class defining all TGA methods used for now."""

    def __init__(self, config_path):
        """Client initialization.

        Args:
            config: Configuration dictionary stored at storage/config.json
        """
        self.config = {}

        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.loads(f.read())
            if not self.config['api_hash'] or not self.config['api_id']:
                self.initialize_auth_config()
        else:
            self.initialize_auth_config()

        self.client = telethon.TelegramClient(self.config['session_path'],
                                              self.config['api_id'],
                                              self.config['api_hash'])

    def initialize_auth_config(self):
        """Config initialization. Needed at first startup."""
        print("""First time hello! Let's configure your TGA""")

        self.config['api_hash'] = input('api_hash: ')
        self.config['api_id'] = int(input('api_id: '))
        self.config['mon_link'] = input('Monitor group invite link: ')
        sess_id = ''.join(random.choices(string.ascii_lowercase, k=8))
        self.config['session_path'] = 'sessions/' + sess_id + '.session'
        self.config['db_path'] = 'storage/' + sess_id + '.db'

        with open('storage/config.json', 'w') as f:
            f.write(json.dumps(self.config))

        conn = sqlite3.connect(self.config['db_path'])
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE messages (msg_id text,
                                                 timestamp text,
                                                 sender_id text,
                                                 message text,
                                                 deleted int)
                        """)

        print("Great! You can edit your configuration at storage/config.json")

    async def verify_auth(self):
        """Auth verification function for testing purposes."""
        await self.client.send_message('me', 'Domo, senpai!')
        me = await self.client.get_me()
        print(me.stringify())





async def main(tga):
    """General program flow for demonstrating modules or creating scenarios.

    Args:
        tga: Telegram Assistant object to perform actions.
    """
    await tga.client.start()

    app = Application()
    app.mainloop()
    print(app.configuration)




    @tga.client.on(telethon.events.MessageDeleted)
    async def save_deleted_messages(event):
        """Save all messages that got deleted into database."""
        for message_id in event.deleted_ids:
            db = sqlite3.connect(tga.config['db_path'])
            cursor = db.cursor()
            cursor.execute(f"""SELECT * FROM messages
                              WHERE msg_id = {message_id}
                              AND deleted = 0
                           """)
            deleted_messages = cursor.fetchall()

            for message in deleted_messages:
                text = message[3]
                sender = message[2]
                log_info = f'-message[{message_id}]: <{text}> from {sender}'
                cursor.execute(f"""UPDATE messages SET deleted = 1
                                  WHERE msg_id = {message_id}
                               """)
                db.commit()

                mon_link = tga.config['mon_link']
                if mon_link:
                    mon_group = await tga.client.get_entity(mon_link)
                    await tga.client.send_message(entity=mon_group,
                                                  message=log_info)

                print(log_info)

    @tga.client.on(telethon.events.NewMessage)
    async def new_msg_handler(event):
        """Save all new messages into database."""
        message_meta = event.message.to_dict()
        message = message_meta['message']
        message_id = str(message_meta['id'])
        sender_id = str(message_meta['from_id']['user_id'])
        timestamp = str(time.time())

        sender = await tga.client.get_entity(int(sender_id))

        row = [(message_id, timestamp, sender.first_name, message, 0)]

        db = sqlite3.connect(tga.config['db_path'])
        cursor = db.cursor()
        cursor.executemany("INSERT INTO messages VALUES (?,?,?,?,?)", row)
        db.commit()

        sender = await tga.client.get_entity(int(sender_id))
        print(f"+message[{message_id}]: <{message}> from {sender.first_name}")

    print("[*] TGA is logged in and listening for events...")
    await tga.client.run_until_disconnected()

if __name__ == '__main__':

    tga = TelegramAssistant(config_path='storage/config.json')
    tga.client.loop.run_until_complete(main(tga))

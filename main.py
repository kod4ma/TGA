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
import tkinter as tk
from tkinter import ttk


class Application(tk.Frame):
    """Class for working with tkinter."""

    def __init__(self, master=None):
        """Initialize of the main window."""
        super().__init__(master)
        self.master.title("TGA ^_^")
        self.master.minsize(width=600, height=400)
        self.master.columnconfigure(3, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.create_widgets()

    def create_widgets(self):
        """Create widgets."""
        self.F = tk.LabelFrame(self.master)
        self.F.grid(sticky='news', columnspan=3, row=0)
        self.F.quit = tk.Button(self.F, text="Применить настройки",
                                command=self.master.destroy)
        self.F.quit.grid(column=3, row=0)

        self.F.quit = tk.Label(self.F)
        self.F.quit["text"] = ("Выберете и настройте модули которын"
                               + "будут запущены    ")
        self.F.quit.grid(column=0, row=0)

        self.f1 = tk.LabelFrame(self.master)
        self.f1.rowconfigure(5, weight=1)
        self.f1.grid(sticky='nsew', column=0, row=1)
        self.f1.newb = tk.Button(self.f1)
        self.f1.newb["text"] = "Включить менеджера"
        self.f1.newb["command"] = self.manage
        self.f1.newb.grid(sticky='nsew', column=0, row=1)
        self.f1.lab = tk.Label(self.f1)
        self.f1.lab["text"] = "Сохранятор выключен"
        self.f1.lab.grid(column=0, row=4)

        self.f2 = tk.LabelFrame(self.master, width=1000, height=100)
        self.f2.rowconfigure(5, weight=1)
        self.f2.grid(sticky='nsew', column=1, row=1)
        self.f2.newb = tk.Button(self.f2)
        self.f2.newb["command"] = self.save_me
        self.f2.newb["text"] = "Включить сохронятор"
        self.f2.newb.grid(column=0, row=0)
        self.f2.lab = tk.Label(self.f2)
        self.f2.lab["text"] = "Сохранятор выключен"
        self.f2.lab.grid(column=0, row=4)

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
        self.f3.off_lab = tk.Label(self.f3)
        self.f3.off_lab["text"] = ("Автоответчик будет включен\n в режимe "
                                   + self.f3.combo.get())
        self.f3.off_lab.grid(column=0, row=4)

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
        self.f3.com_lab.grid(column=0, row=1)
        self.f3.combo = ttk.Combobox(self.f3, values=[
                                    "Все бесят",
                                    "Ночное время",
                                    "Важная встреча",
                                    "Экзамен",
                                    "Детокс"])
        self.f3.combo.current(0)
        self.f3.combo.grid(column=0, row=2)

        self.f3.lab = tk.Label(self.f3)
        self.f3.lab["text"] = "Aвтоответчик будет выключен"
        self.f3.lab.grid(column=0, row=4)

    def save_me(self):
        """Use to start save machine."""
        print("save_me")

    def manage(self):
        """Use to start manage machine."""
        print("manage")


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

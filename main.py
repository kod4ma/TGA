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

        self.client = telethon.TelegramClient(self.config['session_id'],
                                              self.config['api_id'],
                                              self.config['api_hash'])

    def initialize_auth_config(self):
        """Config initialization. Needed at first startup."""
        print("""First time hello! Let's configure your TGA""")

        self.config['api_hash'] = input('api_hash: ')
        self.config['api_id'] = int(input('api_id: '))
        self.config['session_id'] = ''.join(random.choices(
                                            string.ascii_lowercase, k=8))
        self.config['db_path'] = 'storage/' + self.config['session_id'] + '.db'

        with open('storage/config.json', 'w') as f:
            f.write(json.dumps(self.config))

        conn = sqlite3.connect(self.config['db_path'])
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE messages (msg_id text,
                                                 timestamp text,
                                                 sender_id text,
                                                 message text)
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

    @tga.client.on(telethon.events.NewMessage)
    async def new_msg_handler(event):
        """Save all new messages into storage/<session_id>.db."""
        message_meta = event.message.to_dict()
        message = message_meta['message']
        message_id = str(message_meta['id'])
        sender_id = str(message_meta['from_id']['user_id'])
        timestamp = str(time.time())

        row = [(message_id, timestamp, sender_id, message)]

        db = sqlite3.connect(tga.config['db_path'])
        cursor = db.cursor()
        cursor.executemany("INSERT INTO messages VALUES (?,?,?,?)", row)
        db.commit()

        print(f"+message[{message_id}]: <{message}> from {sender_id}")

    print("[*] TGA is logged in and listening for events...")
    await tga.client.run_until_disconnected()

if __name__ == '__main__':

    tga = TelegramAssistant(config_path='storage/config.json')
    tga.client.loop.run_until_complete(main(tga))

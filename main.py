#!/usr/bin/env python3
"""Telegram Assistant is a Telegram daemon that automates user tasks.

TGA is created for simplifying the process of performing routine job
in Telegram Messenger and also for casting some fancy message magic.
"""

import json
import os
import telethon


class TelegramAssistant():
    """A single class defining all TGA methods used for now."""

    def __init__(self, config_path):
        """Client initialization.

        Args:
            config: Configuration dictionary stored at storage/config.json
        """
        self.config = {}

        if (not os.path.exists(config_path) or
                not self.config['api_hash'] or
                not self.config['api_id']):
            self.initialize_auth_config()
        else:
            with open(config_path, 'r') as f:
                self.config = json.loads(f.read())

        self.client = telethon.TelegramClient(self.config['session_id'],
                                              self.config['api_id'],
                                              self.config['api_hash'])

    def initialize_auth_config(self):
        """Config initialization. Needed at first startup."""
        print("""First time hello! Let's configure your TGA""")

        self.config['api_hash'] = input('api_hash: ')
        self.config['api_id'] = int(input('api_id: '))
        self.config['session_id'] = input('session_id: ')
        self.config['session_id_len'] = int(input('session_id_len: '))

        with open('storage/config.json', 'w') as f:
            f.write(json.dumps(self.config))

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
    await tga.verify_auth()

if __name__ == '__main__':

    tga = TelegramAssistant(config_path='storage/config.json')
    tga.client.loop.run_until_complete(main(tga))

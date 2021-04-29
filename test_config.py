import unittest
import pathlib
import json
import re

from telethon import TelegramClient

class TestConfig(unittest.TestCase):

    def setUp(self):
        with open('storage/config.json', 'r') as f:
            self.config = json.loads(f.read())

    def test_1_cfgfile(self):
        path = pathlib.Path('storage/config.json')
        self.assertEqual((str(path), path.is_file()), ('storage/config.json', True))

    def test_2_cfgvalid(self):
        self.assertTrue('api_hash' in self.config)
        self.assertTrue('api_id' in self.config)
        self.assertTrue('session_path' in self.config)
        self.assertTrue('db_path' in self.config)

    def test_3_api_hash(self):
        h = self.config['api_hash']
        self.assertEqual(re.findall(r"([a-fA-F\d]{32})", h)[0], h)
        self.assertEqual(len(h), 32)

    def test_4_api_id(self):
        api_id = self.config['api_id']
        self.assertTrue(type(api_id) == int)

    def test_5_sessfile(self):
        sesspath = self.config['session_path']
        path = pathlib.Path(sesspath)
        self.assertEqual((str(path), path.is_file()), (sesspath, True))

    def test_6_dbfile(self):
        dbpath = self.config['db_path']
        path = pathlib.Path(dbpath)
        self.assertEqual((str(path), path.is_file()), (dbpath, True))

    async def conn(self, client):
        me = await client.get_me()
        self.me = me.first_name


    def test_7_connection(self):
        sess = self.config['session_path']
        api_hash = self.config['api_hash']
        api_id = self.config['api_id']
        client = TelegramClient(sess, api_id, api_hash)

        with client:
            client.loop.run_until_complete(self.conn(client))
            self.assertTrue(len(self.me) > 0)

if __name__ == '__main__':
    unittest.main()

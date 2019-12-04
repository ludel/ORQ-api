import os
import unittest

import requests

from models.user import User

BASE_URL = 'http://localhost:8080'
DB = 'test.db'


class TestSession(unittest.TestCase):
    def setUp(self):
        User.init(DB)

    def test_sign_up(self):
        sign_in_content = {'url': f'{BASE_URL}/session/sign_up/',
                           'json': {'email': 'user@test.com', 'password': 'password'},
                           'headers': {'content-type': 'application/json'}}

        req = requests.post(**sign_in_content)
        self.assertEqual(req.text, 'User created')

        req = requests.post(**sign_in_content)
        self.assertEqual(req.text, 'User already exists')

    def test_sign_in(self):
        sign_in_content = {'url': f'{BASE_URL}/session/sign_in/',
                           'json': {'username': 'user@test.com', 'password': 'password'},
                           'headers': {'content-type': 'application/json'}}

        req = requests.post(**sign_in_content)
        self.assertEqual(req.status_code, 200)

    def tearDown(self):
        os.remove(DB)

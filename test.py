import os
import json
import requests

import unittest
from app import db, create_app
from app.models import User
from config import TestConfig

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='test', email='test_electro@example.com')
        u.set_password('foobar')
        self.assertFalse(u.check_password('barfoo'))
        self.assertTrue(u.check_password('foobar'))

    def test_forgot_otp(self):
        url = 'http://localhost:5000/forgotPassword'

        payload = {
                    'email': 'whatever@mailinator.com'
                }
        json_payload = json.dumps(payload)

        headers = {
                    'Content-Type': 'application/json'
                }
        response = requests.post(url, data=json_payload, headers=headers)
        self.assertTrue(response.status_code == 200)

if __name__ == '__main__':
    unittest.main(verbosity=2)
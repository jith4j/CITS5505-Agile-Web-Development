from app import create_app, db
from config import TestConfig
import multiprocessing
from selenium import webdriver
import time
from app.models import User, Question, Answer, Reply
from unittest import TestCase
import unittest

localHost = "http://localhost:5000/"
from selenium.webdriver.edge.service import Service

def add_test_data_to_db():
    user = User(username='uno', email='uno@example.com')
    db.session.add(user)
    user.set_password('one')
    db.session.commit()

class SeleniumTests(TestCase):
    def setUp(self):
        self.testapp = create_app(TestConfig)
        self.app_context = self.testapp.app_context()
        self.app_context.push()
        db.create_all()
        add_test_data_to_db()

        self.server_thread = multiprocessing.Process(target=self.testapp.run)
        self.server_thread.start()

        edgedriver_path = './app/static/drivers/msedgedriver.exe'
        service = Service(executable_path=edgedriver_path)
        self.driver = webdriver.Edge(service=service)
        self.driver.get(localHost)

    def tearDown(self):
        self.server_thread.terminate()
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_example(self):
        # creating an empty browser
        # with logged in user added
        pass

if __name__ == '__main__':
    unittest.main()
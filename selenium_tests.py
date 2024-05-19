from app import create_app, db
from config import TestConfig
import multiprocessing
from selenium import webdriver
from app.models import User, Question, Answer, Reply
from unittest import TestCase
import unittest

localHost = "http://localhost:5000/"

def add_test_data_to_db():
    user = User(username='uno', email='uno@example.com')
    db.session.add(user)
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

        self.driver = webdriver.Chrome()
        self.driver.get(localHost)

    def tearDown(self):
        self.server_thread.terminate()
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_example(self):
        # Add your test case here
        pass

if __name__ == '__main__':
    unittest.main()

# def test_groups_page(self):
    #     self.driver.get(localHost + "login")
        # for group in Group.query.all():
        # for student in group.students:
        # elems = self.driver.find_elements(By.ID, student.uwa_id)
        # self.assertEquals(
        # len(elems),
        # 1,
        # f"Could not find student {student.uwa_id} on Groups page"
        # )
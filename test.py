import unittest
from app import db, create_app
from app.models import User, Question, Answer, Reply, Like
from config import TestConfig
from datetime import datetime, timezone, timedelta
from flask_login import login_user
import sqlalchemy as sa
from flask import request

def answer(qid):
    ans_list = []
    ans = db.session.scalars(sa.select(Answer).where(Answer.question_id == qid)).all()
    sort_order = request.args.get('sort', 'most_liked')

    for a in ans:
        replies = db.session.scalars(sa.select(Reply).where(Reply.answer_id == a.id)).all()
        likes = db.session.scalars(sa.select(Like).where(Like.answer_id == a.id)).all()
        ans_list.append({
            'answer': a.answer,
            'id': a.id,
            'author': a.author.username,
            'author_avatar': a.author,
            'timestamp': a.timestamp,
            'all_replies': replies,
            'likes': len(likes),
        })

    if sort_order == 'most_liked':
        ans_list.sort(key=lambda a: a['likes'], reverse=True)
    elif sort_order == 'least_liked':
        ans_list.sort(key=lambda a: a['likes'])
    elif sort_order == 'newest':
        ans_list.sort(key=lambda a: a['timestamp'], reverse=True)
    else:
        ans_list.sort(key=lambda a: a['timestamp'])

    return ans_list

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
        with self.app.test_client() as client:
            payload = {
                'email': 'whatever@mailinator.com'
            }
            response = client.post('/login', json=payload)
            self.assertTrue(response.status_code == 200)

    def test_sort_functionality(self):
        u1 = User(username='uno', email='uno@example.com')
        u1.set_password('one')
        u2 = User(username='duo', email='duo@example.com')
        u2.set_password('duo')
        u3 = User(username='tres', email='tres@example.com')
        u3.set_password('tres')
        u4 = User(username='cuatro', email='cuatro@example.com')
        u4.set_password('cuatro')
        db.session.add_all([u1, u2, u3, u4])

        # create a ques, three answers and two replies
        now = datetime.now(timezone.utc)
        q1 = Question(question="Question from uno", author=u1,
                  timestamp=now + timedelta(seconds=1))
        db.session.add(q1)
        a1 = Answer(answer="Answer from duo", author=u2, question=q1,
                  timestamp=now + timedelta(seconds=7))
        a2 = Answer(answer="Answer from tres", author=u3, question=q1,
                  timestamp=now + timedelta(seconds=4))
        a3 = Answer(answer="Answer from cuatro", author=u4, question=q1,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([a1, a2, a3])
        r1 = Reply(reply="Reply from uno", author=u1, question=q1, answer=a2,
                  timestamp=now + timedelta(seconds=2))
        r2 = Reply(reply="Reply from tres", author=u3, question=q1, answer=a2,
                  timestamp=now + timedelta(seconds=7))
        db.session.add_all([r1, r2])
        l1 = Like(user=u2, answer=a2)
        l2 = Like(user=u1, answer=a2)
        l3 = Like(user=u3, answer=a2)
        l4 = Like(user=u4, answer=a1)
        db.session.add_all([l1, l2, l3, l4])
        db.session.commit()

        with self.app.test_request_context('/answer/{}'.format(q1.id)):
            # Set the current user
            login_user(u1)

            # Test most_liked sorting
            with self.app.test_request_context('/answer/{}?sort=most_liked'.format(q1.id)):
                ans_most_liked = answer(q1.id)

            # Test least_liked sorting
            with self.app.test_request_context('/answer/{}?sort=least_liked'.format(q1.id)):
                ans_least_liked = answer(q1.id)

            # Test newest sorting
            with self.app.test_request_context('/answer/{}?sort=newest'.format(q1.id)):
                ans_newest = answer(q1.id)

            # Test oldest sorting (default sorting)
            with self.app.test_request_context('/answer/{}?sort=oldest'.format(q1.id)):
                ans_oldest = answer(q1.id)

            # Perform assertions on the sorted answer lists
            self.assertEqual(len(ans_most_liked), 3)
            self.assertEqual(ans_most_liked[0]['id'], a2.id)
            self.assertEqual(ans_most_liked[1]['id'], a1.id)
            self.assertEqual(ans_most_liked[2]['id'], a3.id)

            self.assertEqual(len(ans_least_liked), 3)
            self.assertEqual(ans_least_liked[0]['id'], a3.id)
            self.assertEqual(ans_least_liked[1]['id'], a1.id)
            self.assertEqual(ans_least_liked[2]['id'], a2.id)

            self.assertEqual(len(ans_newest), 3)
            self.assertEqual(ans_newest[0]['id'], a1.id)
            self.assertEqual(ans_newest[1]['id'], a2.id)
            self.assertEqual(ans_newest[2]['id'], a3.id)

            self.assertEqual(len(ans_oldest), 3)
            self.assertEqual(ans_oldest[0]['id'], a3.id)
            self.assertEqual(ans_oldest[1]['id'], a2.id)
            self.assertEqual(ans_oldest[2]['id'], a1.id)

if __name__ == '__main__':
    unittest.main(verbosity=2)
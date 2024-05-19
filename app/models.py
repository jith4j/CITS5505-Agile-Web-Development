from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import pytz

PERTH_TZ = pytz.timezone('Australia/Perth')

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True, nullable=False)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    question_posts: so.WriteOnlyMapped['Question'] = so.relationship(back_populates='author')
    answer_posts: so.WriteOnlyMapped['Answer'] = so.relationship(back_populates='author')
    all_replies: so.WriteOnlyMapped['Reply'] = so.relationship(back_populates='author')
    liked_answers: so.WriteOnlyMapped['Like'] = so.relationship('Like', back_populates='user')


    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
class Question(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    question: so.Mapped[str] = so.mapped_column(sa.String(140), nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(PERTH_TZ), nullable=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    author: so.Mapped[User] = so.relationship(back_populates='question_posts')
    answers: so.WriteOnlyMapped['Answer'] = so.relationship(back_populates='question')
    all_replies: so.WriteOnlyMapped['Reply'] = so.relationship(back_populates='question')

    def __repr__(self):
        return '<Question{}>'.format(self.question)
    
class Answer(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    answer: so.Mapped[str] = so.mapped_column(sa.String(140), nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(PERTH_TZ), nullable=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    question_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Question.id),
                                               index=True)
    author: so.Mapped[User] = so.relationship(back_populates='answer_posts')
    question: so.Mapped[Question] = so.relationship(back_populates='answers')
    all_replies: so.WriteOnlyMapped['Reply'] = so.relationship(back_populates='answer')
    likes: so.WriteOnlyMapped['Like'] = so.relationship('Like', back_populates='answer')


    def __repr__(self):
        return '<Answer{}>'.format(self.answer)
    
class Reply(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    reply: so.Mapped[str] = so.mapped_column(sa.String(140), nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(PERTH_TZ), nullable=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    question_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Question.id),
                                               index=True)
    answer_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Answer.id),
                                            index=True)
    author: so.Mapped[User] = so.relationship(back_populates='all_replies')
    question: so.Mapped[Question] = so.relationship(back_populates='all_replies')
    answer: so.Mapped[Answer] = so.relationship(back_populates='all_replies')

    def __repr__(self):
        return '<Reply{}>'.format(self.reply)
    
class Like(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    answer_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('answer.id'), nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(PERTH_TZ), nullable=False)
    user: so.Mapped[User] = so.relationship('User', back_populates='liked_answers')
    answer: so.Mapped[Answer] = so.relationship('Answer', back_populates='likes')

    def __repr__(self):
        return f'<Like user_id={self.user_id} answer_id={self.answer_id}>'
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

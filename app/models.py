from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True, nullable=False)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    question_posts: so.WriteOnlyMapped['Question'] = so.relationship(back_populates='author')
    answer_posts: so.WriteOnlyMapped['Answer'] = so.relationship(back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Question(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    question: so.Mapped[str] = so.mapped_column(sa.String(140), nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc), nullable=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    author: so.Mapped[User] = so.relationship(back_populates='question_posts')
    answers: so.WriteOnlyMapped['Answer'] = so.relationship(back_populates='question')

    def __repr__(self):
        return '<Question{}>'.format(self.question)
    
class Answer(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    answer: so.Mapped[str] = so.mapped_column(sa.String(140), nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc), nullable=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    question_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Question.id),
                                               index=True)
    author: so.Mapped[User] = so.relationship(back_populates='answer_posts')
    question: so.Mapped[Question] = so.relationship(back_populates='answers')

    def __repr__(self):
        return '<Answer{}>'.format(self.answer)
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

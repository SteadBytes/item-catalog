from app import db_session
from app import Base
from app.mod_auth.models import User
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    creator_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'created_at': self.created_at,
            'name': self.name,
        }

    @classmethod
    def by_name(cls, category_name):
        return db_session.query(cls).filter_by(name=category_name).first()

    @classmethod
    def by_id(cls, category_id):
        return db_session.query(cls).filter_by(id=category_id).first()


class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    category_id = Column(Integer, ForeignKey('category.id'))
    creator_id = Column(Integer, ForeignKey('user.id'))
    category = relationship(Category)
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'created_at': self.created_at,
            'creator_id': self.creator_id,
            'creator': self.user.name,
            'category': self.category.name,
            'description': self.description,
            'title': self.title,
        }

    @classmethod
    def by_title(cls, item_title):
        return db_session.query(cls).filter_by(title=item_title).first()

    @classmethod
    def by_category(cls, category):
        return db_session.query(cls).filter_by(category_id=category.id).all()

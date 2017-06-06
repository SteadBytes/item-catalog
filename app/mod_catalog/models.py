from app import db_session
from app import Base
from app.mod_auth.models import User
import datetime
from sqlalchemy.orm import relationship, backref
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
        """Returns category given a category name

        Args:
            category_name: String, name of category to retrieve.
        """
        return db_session.query(cls).filter_by(name=category_name).first()

    @classmethod
    def by_id(cls, category_id):
        """Returns category given a category id

        Args:
            category_id: Integer, primary key id of required category.
        """
        return db_session.query(cls).filter_by(id=category_id).first()


class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    category_id = Column(Integer, ForeignKey('category.id'))
    creator_id = Column(Integer, ForeignKey('user.id'))
    category = relationship(Category, backref=backref(
        "items", cascade="all, delete-orphan"))
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
        """Returns item given a title

        Args:
            item_title: String, title of item to retrieve.
        """
        return db_session.query(cls).filter_by(title=item_title).first()

    @classmethod
    def by_category(cls, category):
        """Returns all items for a given category

        Args:
            category: Category Object to filter items by
        """
        return db_session.query(cls).filter_by(category_id=category.id).all()

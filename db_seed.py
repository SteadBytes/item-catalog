from flask import Flask
from sqlalchemy import *
from app.mod_auth.models import User
from app.mod_catalog.models import Category, Item
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Used for seeding the database with test datafor testing and dev purposes

Base = declarative_base()

engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Clear the tables
session.query(Category).delete()
session.query(Item).delete()

# Add categories
sample_categories = ['Sports', 'Entertainment', 'Tech']

for category_name in sample_categories:
    category = Category(name=category_name)
    session.add(category)
session.commit()

# Add items
sample_items = {'Bat': 1, 'TV': 2, 'Computer': 3}

for name, category in sample_items.items():
    item = Item(title=name, description="Sample description",
                category_id=category, creator_id=1)
    session.add(item)
session.commit()

session.add(item)
session.commit()

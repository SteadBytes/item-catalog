# Import flask and template operator
from flask import Flask, render_template, url_for, redirect

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# set config
app.config.from_object('config')

# Define database object for use in modules/controllers
# db = SQLAlchemy(app)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

from flask_login import (LoginManager, login_required, login_user,
                         logout_user, current_user
                         )
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"


# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_catalog.controllers import mod_catalog as catalog_module
from app.mod_api.controllers import mod_api as api_module
# Register blueprint(s)
app.register_blueprint(auth_module)  # authentication ->google login
app.register_blueprint(catalog_module)  # main catalog
app.register_blueprint(api_module)  # JSON API endpoint


@app.route('/')
@app.route('/catalog')
def index():
    return redirect(url_for('catalog.home'))


# Import Category model for inject_categories context processor below
from app.mod_catalog.models import Category


@app.context_processor
def inject_categories():
    """Flask/Jinja2 template context processor to inject all current
        categories into all templates
    """
    categories = db_session.query(Category).all()
    return dict(categories=categories)


Base.metadata.create_all(engine)

# Import flask and template operator
from flask import Flask, render_template

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

from flask_login import LoginManager, login_required, login_user, logout_user, current_user
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"


@app.route('/')
@login_required
def index():
    return render_template('index.html.j2')


# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module

# Register blueprint(s)
app.register_blueprint(auth_module)

# Build the database:
# This will create the database file using SQLAlchemy
# db_session.create_all()

Base.metadata.create_all(engine)

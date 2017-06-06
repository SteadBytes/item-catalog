# Enable dev environment
DEBUG = True

# Define app directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    os.path.join(BASE_DIR, 'item_catalog.db')
DATABASE_CONNECT_OPTIONS = {}


# Protection against CSRF attacks
CSRF_ENABLED = True

CSRF_SESSION_KEY = 'verysecret'

# Secret for sigining cookies
SECRET_KEY = 'secretkey'

CLIENT_ID = "CLIENT_ID_HERE"
CLIENT_SECRET = "CLIENT_SECRET_HERE"
REDIRECT_URI = "https://localhost:5000/auth/gcallback"
AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
SCOPE = ['profile', 'email']

from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for
from app import db_session
from app import app
import json
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError
from flask_login import login_required, login_user, logout_user, current_user
from app import login_manager
# Import module models (i.e. User)
from app.mod_auth.models import User
# Define Blueprint
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

CLIENT_ID = app.config['CLIENT_ID']
REDIRECT_URI = app.config['REDIRECT_URI']
AUTH_URI = app.config['AUTH_URI']


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    Args:
        user_id: user_id (email) user to retrieve
    Returns:
        User object
    """
    return db_session.query(User).filter_by(email=user_id).first()


def get_google_auth(state=None, token=None):
    """Create OAuth2Session object w/given arguments

    With no params provided, generates new OAuth2Session with a new state.
    If state is provided, gets a token.
    If token provided,gets an OAuth access token with correct scope->final step
    """
    if token:
        return OAuth2Session(CLIENT_ID, token=token)
    if state:
        return OAuth2Session(CLIENT_ID, state=state, redirect_uri=REDIRECT_URI)
    oauth = OAuth2Session(
        CLIENT_ID, redirect_uri=REDIRECT_URI, scope=app.config['SCOPE'])
    return oauth


@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('catalog.home'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return render_template('auth/signin.html.j2', auth_url=auth_url)


@mod_auth.route('/gcallback')
def callback():
    """google sign-in callback function used by OAuth2 API

    Handles user info for auht app via google OAuth2. If user has successfully
    authenticated the app and access token is retrieved and the users info is
    returned from google.
    User data is accessed and stored appropriately in database.
    """
    # Redirect to homepage if already logged in
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('catalog.home'))
    # Check URL for error query parameter
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return "Access denied"
        return "Error encountered"
    if 'code' not in request.args and 'state' not in request.args:
        # URL accessed directly not through login flow:redirect to login
        return redirect(url_for('auth.login'))
    else:
        # Successful authencation for app
        google = get_google_auth(state=session['oauth_state'])
        try:
            # Get access token from google
            token = google.fetch_token(
                app.config['TOKEN_URI'],
                client_secret=app.config['CLIENT_SECRET'],
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occured'
        google = get_google_auth(token=token)
        resp = google.get(app.config['USER_INFO'])
        if resp.status_code == 200:
            # get user data from JSON response
            user_data = resp.json()
            email = user_data['email']
            user = db_session.query(User).filter_by(email=email).first()
            # If user doesn't already exist,add to DB
            if user is None:
                user = User()
                user.email = email
            user.name = user_data['name']
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            user.authenticated = True
            db_session.add(user)
            db_session.commit()
            login_user(user)
            return redirect(url_for('catalog.home'))
        return 'Couldnt fetch user information'


@mod_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('catalog.home'))

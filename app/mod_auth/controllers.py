# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for
from app import app
import json
# Import the database object from the main app module
from app import db_session
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

    :param unicode user_id: user_id (email) user to retrieve
    """
    return db_session.query(User).filter_by(email=user_id).first()


def get_google_auth(state=None, token=None):
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
        return redirect(url_for('index'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return render_template('auth/signin.html.j2', auth_url=auth_url)


@mod_auth.route('/gcallback')
def callback():
    # Redirect to homepage if logged in
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return "Access denied"
        return "Error encountered"
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('auth.login'))
    else:
        # Successful authencation for app
        google = get_google_auth(state=session['oauth_state'])
        try:
            token = google.fetch_token(
                app.config['TOKEN_URI'], client_secret=app.config['CLIENT_SECRET'], authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occured'
        google = get_google_auth(token=token)
        resp = google.get(app.config['USER_INFO'])
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = db_session.query(User).filter_by(email=email).first()
            if user is None:
                user = User()
                user.email = email
            user.name = user_data['name']
            print(token)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            user.authenticated = True
            db_session.add(user)
            db_session.commit()
            login_user(user)
            return redirect(url_for('index'))
        return 'Couldnt fetch user information'


@mod_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

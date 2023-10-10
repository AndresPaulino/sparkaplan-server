from flask import Blueprint, redirect, url_for, session, jsonify, request
from flask_oauthlib.client import OAuth
from models.user import User

google_auth_blueprint = Blueprint('google_auth', __name__)

oauth = OAuth()
google = oauth.remote_app(
    'google',
    consumer_key='YOUR_GOOGLE_CLIENT_ID',
    consumer_secret='YOUR_GOOGLE_CLIENT_SECRET',
    request_token_params={
        'scope': 'email profile'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@google_auth_blueprint.route('/login-google')
def login_google():
    return google.authorize(callback=url_for('.authorized', _external=True))

@google_auth_blueprint.route('/login-google/callback')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    user = User.find_or_create_by_google(
        google_id=user_info.data["id"],
        email=user_info.data["email"],
        first_name=user_info.data["given_name"],
        last_name=user_info.data["family_name"]
    )
    # Now generate a JWT for this user or set them as logged in.
    # ... your JWT generation/login code ...

    return jsonify(user_info.data)

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

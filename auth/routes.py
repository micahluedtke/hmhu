from flask import Blueprint, request, redirect, abort, jsonify, make_response, url_for

import time, datetime
from firebase_admin import auth

authentication = Blueprint('auth', __name__, static_folder='static')

@authentication.route('/login')
def login():
    return authentication.send_static_file('login.html')

@authentication.route('/logout')
def logout():
    session_cookie = request.cookies.get('session')
    try:
        # revoke session with Firebase
        decoded_claims = auth.verify_session_cookie(session_cookie)
        auth.revoke_refresh_tokens(decoded_claims['sub'])

        # clear session cookie
        response = make_response(redirect(url_for('.login')))
        response.set_cookie('session', expires=0)
        print(response)
        return response
    except auth.InvalidSessionCookieError:
        return redirect(url_for('.login'))

@authentication.route('/token', methods=['POST'])
def client_ID_to_session_token():
    # Get the ID token sent by the client
    id_token = request.json['idToken']

    # Set session expiration to 5 days.
    expires_in = datetime.timedelta(days=5)

    # To ensure that cookies are set only on recently signed in users, check auth_time in ID token before creating a cookie.
    try:
        decoded_claims = auth.verify_id_token(id_token)
        # Only process if the user signed in within the last 5 minutes.
        if time.time() - decoded_claims['auth_time'] < 5 * 60:
            expires_in = datetime.timedelta(days=5)
            expires = datetime.datetime.now() + expires_in
            session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
            response = jsonify({'status': 'success'})
            response.set_cookie(
                'session', session_cookie, expires=expires, httponly=False, secure=False)
            return response
        # User did not sign in recently. To guard against ID token theft, require
        # re-authentication.
        return abort(401, 'Recent sign in required')
    except auth.InvalidIdTokenError:
        return abort(401, 'Invalid ID token')
    except:
        return abort(401, 'Failed to create a session cookie')


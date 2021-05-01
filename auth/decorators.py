from functools import wraps
from flask import request, redirect, url_for
from firebase_admin import auth

def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        session_cookie = request.cookies.get('session')
        if not session_cookie:
            # Session cookie is unavailable. Force user to login.
            return redirect(url_for('auth.login'))

        # Verify the session cookie. In this case an additional check is added to detect
        # if the user's Firebase session was revoked, user deleted/disabled, etc.
        try:
            request.user = auth.verify_session_cookie(session_cookie, check_revoked=True)
        except auth.InvalidSessionCookieError:
            # Session cookie is invalid, expired or revoked. Force user to login.
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)
    return decorated_function

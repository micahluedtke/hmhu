from flask              import Flask, redirect, render_template
from flask_bootstrap    import Bootstrap

import firebase_admin
from firebase_admin     import credentials, firestore

#import for login capabilties
from auth.routes import authentication
from auth.decorators import login_required


app = Flask(__name__)
Bootstrap(app)

# connect to db using firebase either here or through the firebase.py file

# Use a service account
# cred = credentials.Certificate('./hmhu-ecds-firebase-admin-cred.json')
# firebase_admin.initialize_app(cred)
firebase_admin.intialize_app()

from question           import question
from answer             import answer
from myanswer           import myanswer
from resources          import resources

# register blueprints
app.register_blueprint(question)
app.register_blueprint(answer)
app.register_blueprint(myanswer)
app.register_blueprint(resources)
app.register_blueprint(authentication, url_prefix='/auth')

# the default route is index
@app.route('/')
@login_required
def default():    
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

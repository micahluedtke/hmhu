from flask              import Flask, redirect, render_template
from flask_bootstrap    import Bootstrap
from question           import question
from answer             import answer
import firebase_admin
from firebase_admin     import credentials, firestore


app = Flask(__name__)
Bootstrap(app)

# connect to db using firebase either here or through the firebase.py file

# Use a service account
cred = credentials.Certificate('./hmhu-ecds-firebase-adminsdk-kbx6m-1c922e1a60.json')
firebase_admin.initialize_app(cred)

@app.route('/home')
def home():
    db = firestore.client()
    doc_id = 'rHeE12HG8nPHhnA6pj2c'
    # questions = db.collection(u'questions').stream()
    # questions = [(doc.id, doc.to_dict()) for doc in questions]
    # return questions[2]
    doc_ref = db.collection(u'questions').document(doc_id)
    doc = doc_ref.get()
    if doc.exists:
        return f'Document data: {doc.to_dict()}'
    else:
        return 'No such document!'

# register blueprints
app.register_blueprint(question)
app.register_blueprint(answer)

# the default route is index
@app.route('/')
def default():    
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Blueprint, render_template
import firebase_admin
from firebase_admin     import firestore

# blueprint setup
answer = Blueprint('answer', __name__)

db = firestore.client()

@answer.route('/answer')
def default():
    doc_id = 'rHeE12HG8nPHhnA6pj2c'
    answer_docs = db.collection('questions').document(doc_id).collection('answers').stream()
    answers = [(doc.id, doc.to_dict()) for doc in answer_docs]
    return render_template('answer/index.html', list=answers)

    


# firestore.SERVER_TIMESTAMP
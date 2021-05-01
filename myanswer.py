from flask import Blueprint, render_template, request, redirect
import firebase_admin
from firebase_admin     import firestore
#import for login capabilties
from auth.routes import authentication
from auth.decorators import login_required

# blueprint setup
myanswer = Blueprint('myanswer', __name__)

db = firestore.client()

@myanswer.route('/myanswer')
@login_required
def default():
    questions = db.collection('questions').stream()
    questions = [(doc.id, doc.to_dict()['question_text']) for doc in questions]
    my_id = request.user['uid']
    question_answers = {}
    for question in questions:
        doc_id = question[0]
        doc_text = question[1]
        answer_ref = db.collection('questions').document(doc_id).collection('answers')
        query_ref = answer_ref.where('user', '==',my_id).stream()
        answers = [ doc.to_dict()['answer'] for doc in query_ref]
        question_answers[doc_text] = answers
        
    return render_template('answer/index.html', list=question_answers)
    



# firestore.SERVER_TIMESTAMP
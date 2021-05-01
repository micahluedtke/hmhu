from flask import Blueprint, render_template
import firebase_admin
from firebase_admin     import firestore
#import for login capabilties
from auth.routes import authentication
from auth.decorators import login_required

# blueprint setup
answer = Blueprint('answer', __name__)

db = firestore.client()

@answer.route('/answer')
def default():
    questions = db.collection('questions').stream()
    questions = [(doc.id, doc.to_dict()['question_text']) for doc in questions]
    question_answers = {}
    for question in questions:
        doc_id = question[0]
        doc_text = question[1]
        answer_ref = db.collection('questions').document(doc_id).collection('answers')
        query_ref = answer_ref.where('share', '==','1').stream()
        answers = [doc.to_dict()['answer'] for doc in query_ref]
        question_answers[doc_text] = answers
    print(question_answers)
    return render_template('answer/index.html', list=question_answers)
    



# firestore.SERVER_TIMESTAMP
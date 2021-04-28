from flask import Blueprint, render_template, request, redirect
import firebase_admin
from firebase_admin     import firestore
import random

# blueprint setup
question = Blueprint('question', __name__)


db = firestore.client()

@question.route('/question')
#the way this is currently written only the question text is getting passed to the html template, so the form won't know the doc.id to pass back when an answer is submitted
def default():
    #stream questions collection from firestore
    questions = db.collection('questions').stream()
    #create a list of all question_texts 
    questions = [(doc.id, doc.to_dict()['question_text']) for doc in questions]
    #randomly select a question from the list of quetions
    qid, question = random.choice(questions)
    users = db.collection('users').stream()
    users = [doc.id for doc in users]
    return render_template('question/index.html', question=question, qid=qid, users=users)

@question.route('/submitanswer', methods=['POST'])
def submitanswer():
    answer = request.form
    qid = answer['qid']
    answer_text = answer['answer']
    user = answer['user']
    db = firestore.client()
    answer_ref = db.collection('questions').document(qid).collection('answers')
    answer_ref.add({'answer':answer_text, 'user': user, 'timestamp':firestore.SERVER_TIMESTAMP})
    return redirect('/answer')
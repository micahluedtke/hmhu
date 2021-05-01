from flask import Blueprint, render_template, request, redirect
import firebase_admin
from firebase_admin     import firestore
import random

#import for login capabilties
from auth.routes import authentication
from auth.decorators import login_required

# blueprint setup
question = Blueprint('question', __name__)


db = firestore.client()

@question.route('/question')
@login_required
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
    print(request.user)
    return render_template('question/index.html', question=question, qid=qid, users=users)

@question.route('/submitanswer', methods=['POST'])
@login_required
def submitanswer():
    answer = request.form
    qid = answer['qid']
    answer_text = answer['answer']
    db = firestore.client()
    user = request.user['uid']
    answer_ref = db.collection('questions').document(qid).collection('answers')
    answer_ref.add({'answer':answer_text, 'user': user, 'timestamp':firestore.SERVER_TIMESTAMP})
    return redirect('/answer')


@question.route('/finishSignUp')
@login_required
def signup():
    # check if user is in DB
    db = firestore.client()
    user_ref = db.collection('users').document(request.user['uid'])
    user = user_ref.get()
    # print(request.user['uid'])
    if user.exists:
        return redirect('/question')
    else:
        db.collection('users').document(request.user['uid']).set({'signup':firestore.SERVER_TIMESTAMP, 'email':request.user['email']})
        return redirect('/question')
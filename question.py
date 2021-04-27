from flask import Blueprint, render_template
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
    questions = db.collection(u'questions').stream()
    #create a list of all question_texts 
    questions = [doc.to_dict()['question_text'] for doc in questions]
    #randomly select a question from the list of quetions
    question = [random.choice(questions)]
    return render_template('question/index.html', list=question)

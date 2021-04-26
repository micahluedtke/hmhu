from flask import Blueprint, render_template

# blueprint setup
question = Blueprint('question', __name__)

# db = firestore.client()

@question.route('/question')
def default():
    render_template('question/index.html')
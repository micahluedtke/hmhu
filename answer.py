from flask import Blueprint, render_template

# blueprint setup
answer = Blueprint('answer', __name__)

@answer.route('/answer')
def default():
    return render_template('answer/index.html')

    

from flask              import Flask, redirect, render_template
from flask_bootstrap    import Bootstrap
from question           import question
from answer             import answer

app = Flask(__name__)
Bootstrap(app)

# connect to db using firebase either here or through the firebase.py file

# register blueprints
app.register_blueprint(question)
app.register_blueprint(answer)

# the default route is index
@app.route('/')
def default():    
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
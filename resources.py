from flask import Blueprint, render_template, request, redirect
import firebase_admin
from firebase_admin     import firestore
import random

#import for login capabilties
from auth.routes import authentication
from auth.decorators import login_required

# blueprint setup
resources = Blueprint('resources', __name__)


db = firestore.client()

@resources.route('/resources')
def default():
    resources = db.collection('resources').stream()
    resources = [doc.id for doc in resources]
    resource_dict = {}
    for resource in resources:
        help_ref = db.collection('resources').document(resource).collection('help').stream()
        help = [doc.to_dict()['url'] for doc in help_ref]
        resource_dict[resource] = help
        
    return render_template('answer/index.html', list=resource_dict)
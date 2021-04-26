import firebase_admin
from firebase_admin import credentials, firestore

# Use a service account
cred = credentials.Certificate('./hmhu-ecds-firebase-adminsdk-kbx6m-1c922e1a60.json')
firebase_admin.initialize_app(cred)

db = firestore.client()



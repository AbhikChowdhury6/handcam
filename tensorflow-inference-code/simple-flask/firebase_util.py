from google.cloud import storage
import os
import jwt
from firebase import firebase

# client = None
# bucket = None
# imageBlob = None

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="key.json"
firebase = firebase.FirebaseApplication('https://mainaskhands.firebaseio.com/')
client = storage.Client()
bucket = client.get_bucket('mainaskhands.appspot.com')
# posting to firebase storage
imageBlob = bucket.blob("/")
print('firebase initialized')

def init_firebase():

	# global client
	# global bucket
	# global imageBlob
	# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="key.json"
	# firebase = firebase.FirebaseApplication('https://mainaskhands.firebaseio.com/')
	# client = storage.Client()
	# bucket = client.get_bucket('mainaskhands.appspot.com')
	# # posting to firebase storage
	# imageBlob = bucket.blob("/")
	print('firebase initialized')

def uploadToFirebase(class_name, image_list):
	for image in image_list:
		filename = image[image.rfind('/')+1:image.rfind('.')+4]
		imageBlob = bucket.blob("uploads/" + class_name + "/" +filename)
		imageBlob.upload_from_filename(image)
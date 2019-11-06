from flask import Flask, flash, request, redirect, render_template
from flask_restful import Resource, Api
from tensorflow_util import init_tensorflow, infer
import urllib.request
import os
import cv2




app = Flask(__name__, static_url_path='')
app.secret_key = "blah blah"
api = Api(app)

UPLOAD_FOLDER = 'uploads'

def init():
	print('tensorflow initialization...')
	init_tensorflow()

init()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# dummy method that takes in an image from file upload
@app.route('/upload', methods=['POST'])
def file_upload():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		filename = file.filename
		upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(upload_path)
		flash('File successfully uploaded')

		#image processing function called
		process(upload_path)
		return redirect('/')

# image processing function that calls the tensorflow oject detection api
def process(img_path):
	im = cv2.imread(img_path)
	print(im.shape)
	#infer function is the tensorflow object detection API function
	object_class = infer(im)
	# results printed to the console. Then the user is redirected back to the main page
	print("object class::", object_class)
	return object_class 

@app.route('/')
def hello_world():
	return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, flash, request, redirect, render_template
from flask_restful import Resource, Api
from tensorflow_util import init_tensorflow, infer
import urllib.request
import os
import cv2
import glob
import operator



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

def multiple_img_infer(directory_path, img_ext = ".jpg"):
	files = glob.glob(directory_path + os.sep + "*" + img_ext)
	class_details = {'specs':{}, 'card':{}, 'keys':{}}
	class_count = {'specs':0, 'card':0, 'keys':0}
	for file in files:
		filename = file[file.rfind('/')+1:file.rfind('.')]
		im = get_img_arr(file)
		inference_result = infer(im)
		print("detection:::", inference_result)
		object_class = inference_result['class']
		if object_class in class_count:
			class_count[object_class]+=1
			class_details[object_class][filename] = inference_result['confidence']
	sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
	final_class = sorted_class_count[0][0]
	frames = []
	class_frame_details = class_details[final_class]
	sorted_frame_details = sorted(class_frame_details.items(), key=operator.itemgetter(1), reverse=True)
	print(sorted_frame_details)
	for i in range(3):
		frames.append(directory_path + "/" + sorted_frame_details[i][0] + img_ext)	 	
	return {"class": final_class, "frames":frames}
	

def get_img_arr(img_path):
	return cv2.imread(img_path)

# image processing function that calls the tensorflow oject detection api
def process(img_path):
	im = get_img_arr(img_path)
	print(im.shape)
	#infer function is the tensorflow object detection API function
	object_class = infer(im)
	# results printed to the console. Then the user is redirected back to the main page
	print("object class::", object_class)
	return object_class 

@app.route('/')
def hello_world():
	res = multiple_img_infer('/home/peps/Class-Files/simple-flask/uploads')
	print(res)
	return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

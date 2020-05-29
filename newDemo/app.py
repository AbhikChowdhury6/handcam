import base64
import json
from io import BytesIO
import sqlite3
import time
import os

import numpy as np
import requests
from flask import Flask, request, jsonify, render_template
#from keras.applications import inception_v3
from keras.preprocessing import image
#from firebase_util import uploadToFirebase

import cv2
import glob
import operator


#from flask import Flask, flash, request, redirect, render_template
#from flask_restful import Resource, Api
from tensorflow_util import init_tensorflow, infer



# from flask_cors import CORS


app = Flask(__name__, static_url_path='')
app.secret_key = "blah blah"
#api = Api(app)

#UPLOAD_FOLDER = 'uploads'

def init():
	print('tensorflow initialization...')
	init_tensorflow()

init()

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# image processing function that calls the tensorflow oject detection api
def process(img_path):
	im = cv2.imread(img_path)
	print(im.shape)
	#infer function is the tensorflow object detection API function
	object_class = infer(im)
	# results printed to the console. Then the user is redirected back to the main page
	print("object class::", object_class)
	return object_class 

# Uncomment this line if you are making a Cross domain request
# CORS(app)


def multiple_img_infer(directory_path, img_ext = ".jpg"):
	files = glob.glob(directory_path + os.sep + "*" + img_ext)
	class_details = {'specs':{}, 'card':{}, 'keys':{}}
	class_count = {'specs':0, 'card':0, 'keys':0}
	is_object = False
	for file in files:
		filename = file[file.rfind('/')+1:file.rfind('.')]
		im = get_img_arr(file)
		inference_result = infer(im)
		print("detection:::", inference_result)
		object_class = inference_result['class']
		if object_class in class_count:
			is_object = True
			class_count[object_class]+=1
			class_details[object_class][filename] = inference_result['confidence']
	if is_object == False:
		return {"class":"None", "frames":[]}
	sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
	final_class = sorted_class_count[0][0]
	frames = []
	class_frame_details = class_details[final_class]
	sorted_frame_details = sorted(class_frame_details.items(), key=operator.itemgetter(1), reverse=True)
	print(sorted_frame_details)
	for i in range(min(3, len(sorted_frame_details))):
		frames.append(directory_path + "/" + sorted_frame_details[i][0] + img_ext)	 	
	return {"class": final_class, "frames":frames}
	

def get_img_arr(img_path):
	return cv2.imread(img_path)


# Testing URL
@app.route('/hello/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello, World!'

@app.route('/makedb/', methods=['GET', 'POST'])
def make_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE objects (type TEXT, uri TEXT, created_at datetime DEFAULT CURRENT_TIMESTAMP)')
    print("Table created successfully")
    conn.close()
    return 'Made DB'

@app.route('/query/', methods=['GET', 'POST'])
def query_db():
    #query DB for the File URI for the most recent instance of that object
    if request.method == 'POST':
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT user_id, MAX(created_at) FROM objects GROUP BY user_id")
   
        URI = cur.fetchall()
        print(URI)
    return send_file("data/" + URI, mimetype='image/jpg')# The image requested


@app.route('/upload/', methods=['POST'])
def image_classifier():
    print("hit the method!")
    # Decoding and pre-processing base64 image

    URI="serverData/" + str(time.time())
    print(URI)
    
    try:
        os.makedirs(URI)
    except OSError:
        print ("Creation of the directory %s failed" % URI)
    else:
        print ("Successfully created the directory %s" % URI)


    c = int(request.form['count'])
    i=0
    for i in range(c):
        rawImg = image.load_img(BytesIO(base64.b64decode(request.form[str(i)])),target_size=(480, 480))
        rawImg.save(URI + "/" + str(time.time()) + ".jpg")
        i = i + 1



    #*********update to save all of the images to a file
    #####save image with uuid and time discriptor



    res = multiple_img_infer(URI)
    print(res)
    frames = res["frames"]
    pred = res["class"]
    #uploadToFirebase(pred, frames)


    #####form sqlite entry using the predicted class
    with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO objects (type,URI) VALUES (?,?)",(str(pred),URI) )
            
            con.commit()
            msg = "Record successfully added"


    # Returning JSON response to the frontend
    return "OK"


@app.route('/test/', methods=['POST'])
def test():
    print("hit the test!")
    # Decoding and pre-processing base64 image
    rawImg = image.load_img(BytesIO(base64.b64decode(request.form['b64'])),target_size=(480, 480))
    img = image.img_to_array(rawImg) / 255.


    #####save image with uuid and time discriptor
    URI="data/" + time.asctime() + ".jpg"
    print(URI)
    rawImg.save(URI)
    print("tried to save")
    return "got it!"
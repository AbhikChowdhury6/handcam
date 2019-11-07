import base64
import json
from io import BytesIO
import sqlite3
import time

import numpy as np
import requests
from flask import Flask, request, jsonify, render_template
#from keras.applications import inception_v3
#from keras.preprocessing import image



# from flask_cors import CORS

app = Flask(__name__)


# Uncomment this line if you are making a Cross domain request
# CORS(app)

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
    rawImg = image.load_img(BytesIO(base64.b64decode(request.form['b64'])),target_size=(480, 480))
    img = image.img_to_array(rawImg) / 255.


    #####save image with uuid and time discriptor
    URI="data/" + time.asctime() + ".jpg"
    print(URI)
    rawImg.save(URI)
    print("tried to save")
    # this line is added because of a bug in tf_serving(1.10.0-dev)
    img = img.astype('float16')

    # Creating payload for TensorFlow serving request
    payload = {
        "instances": [{'input_image': img.tolist()}]
    }

    # Making POST request
    r = requests.post('http://localhost:9000/v1/models/ImageClassifier:predict', json=payload)
    print(r)
    # Decoding results from TensorFlow Serving server
    pred = json.loads(r.content.decode('utf-8'))

    #####form sqlite entry using the predicted class
    with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO objects (type,URI) VALUES (?,?)",(str(pred),URI) )
            
            con.commit()
            msg = "Record successfully added"


    # Returning JSON response to the frontend
    return "I saw some ?",(str(pred))


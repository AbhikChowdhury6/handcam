from __future__ import print_function
import argparse
import contextlib
import datetime
import os
import six
import sys
import time
import unicodedata
import zipfile
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

from werkzeug.utils import secure_filename

app = Flask(__name__)


def file_upload(pathfile):
    zip = zipfile.ZipFile(pathfile)
    zippedfilenames = (zip.namelist())
    for i in range(0,len(zippedfilenames)):
        print(zippedfilenames[i])
        str = zippedfilenames[i]
        timestr = str.split(' ')
        day = timestr[0].split('-')[0];
        month = timestr[0].split('-')[1];
        year = timestr[0].split('-')[2];
        hour = timestr[1].split('.')[0];    
        minute = timestr[1].split('.')[1];
        seconds = timestr[1].split('.')[2];
        print(hour)


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link/')
def my_link():
  print('I got clicked!')
  return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(filename)
            print (url_for('upload_file',
                                    filename=filename))
            file_upload(file)
            return redirect(url_for('upload_file', filename=filename))
    return


if __name__ == '__main__':
  app.run(debug=False)
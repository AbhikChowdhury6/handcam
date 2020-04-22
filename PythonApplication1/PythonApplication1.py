from __future__ import print_function
import argparse
import contextlib
from datetime import datetime
import os
import six
import sys
import time
import unicodedata
import zipfile
import mysql.connector
import platform
from flask import Flask, render_template, request, redirect, url_for

from werkzeug.utils import secure_filename

app = Flask(__name__)


def creationdate(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime
def file_upload(pathfile):
    zip = zipfile.ZipFile(pathfile)
    zippedfilenames = (zip.namelist())
    zip.extractall()
    for name in zip.namelist():
        timemmodified = zip.getinfo(name).date_time
        timeinstr = str(timemmodified[0])+"-"+str(timemmodified[1])+"-"+str(timemmodified[2])+"   "+str(timemmodified[3])+":"+str(timemmodified[4])+":"+str(timemmodified[5])
        #timeinstr = time.strftime("%Y-%m-%d %H:%M:%S", timemmodified)
        data = zip.read(name)
        print(name)
        print(timemmodified)
        print(timeinstr)
    #for i in range(0,len(zippedfilenames)):
        #print(zippedfilenames[i])
        #str = zippedfilenames[i]
        #timestr = str.split(' ')
        #day = timestr[0].split('-')[0];
        #month = timestr[0].split('-')[1];
        #year = timestr[0].split('-')[2];
        #hour = timestr[1].split('.')[0];    
        #minute = timestr[1].split('.')[1];
        #seconds = timestr[1].split('.')[2];
        #mtime = creationdate(zippedfilenames[i])
        #print(mtime)


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
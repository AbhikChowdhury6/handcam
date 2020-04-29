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
import cv2
from subprocess import  check_output, CalledProcessError, STDOUT 

from flask import Flask, render_template, request, redirect, url_for

from werkzeug.utils import secure_filename
app = Flask(__name__)
data=[]
videonums=[]
def get_length(filename):
    command = [
        'ffprobe', 
        '-v', 
        'error', 
        '-show_entries', 
        'format=duration', 
        '-of', 
        'default=noprint_wrappers=1:nokey=1', 
        filename
      ]

    try:
        output = check_output( command, stderr=STDOUT ).decode()
    except CalledProcessError as e:
        output = e.output.decode()
    return output
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
    zip.extractall('temp')
    intcounter =0
    for name in zip.namelist():
        '''timemmodified = zip.getinfo(name).date_time
        #timeinstr = str(timemmodified[0])+"-"+str(timemmodified[1])+"-"+str(timemmodified[2])+"   "+str(timemmodified[3])+":"+str(timemmodified[4])+":"+str(timemmodified[5])
        dt_obj =datetime(*timemmodified[0:6])
        timeinstr = dt_obj
        print(name)
        print(timemmodified)
        vidcapture = cv2.VideoCapture(name)
        fps = vidcapture.get(cv2.CAP_PROP_FPS)
        totalNoFrames = vidcapture.get(cv2.CAP_PROP_FRAME_COUNT);
        durationInSeconds = float(totalNoFrames) / float(fps)
        print("durationInSeconds: ",durationInSeconds,"s")
        durationofvideo = int(durationInSeconds)'''
        #durationofvideo = time.strftime("%Y-%m-%d %H:%M:%S",clip.duration'''
        timemodified = name.split('-')[0].replace('.',':')
        dt_obj = datetime.strptime(timemodified, '%H:%M').time()
        timeinstr = dt_obj
        if name.split('-')[1] not in videonums:
            data.append(dt_obj)
            videonums.append(name.split('-')[1])
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Emma150799!",
            database="testdb"
            )
        mycursor = mydb.cursor()
        #mycursor.execute("CREATE TABLE videos (title VARCHAR(255) PRIMARY KEY, url VARCHAR(255), timecreated DATETIME(6), durationinseconds INT(255))")
        '''if(zip.namelist()[intcounter+1]!=name.split('-')[1]):
            mysqlcommand = "INSERT INTO videos(title,url,timecreated,durationinseconds) VALUES (%s,%s,%s,%s)"
            start_time = data[len(data)-1]
            stop_time = dt_obj
            date = datetime.strptime('24052010', "%d%m%Y").date()
            datetime1 = datetime.combine(date, start_time)
            datetime2 = datetime.combine(date, stop_time)
            durationofvideo = datetime1 - datetime2
            video1 = (name,"fakeurl",timeinstr,durationofvideo)
            mycursor.execute(mysqlcommand,video1)
            mycursor.execute("SELECT * FROM videos")
            for tb in mycursor:
                print(tb)
            mydb.commit()'''
        intcounter = intcounter+1
            
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
    #data = ["4:00 AM","4:00 AM","4:00 AM","4:00 AM","4:00 AM"]
    return render_template('index.html', data = data)

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
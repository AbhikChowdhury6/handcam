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
#import cv2
from fnmatch import fnmatch
from subprocess import check_output, CalledProcessError, STDOUT

from flask import Flask, render_template, request, redirect, url_for

from werkzeug.utils import secure_filename

app = Flask(__name__)
data=[]
imagedata=[]
imagedatacopy=[]
videonums=[]
allfilenamesindatetime=[]
global staticcurrentvideotime
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
        output = check_output(command, stderr=STDOUT).decode()
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
    zip.extractall('static/temp')
    dirname = os.path.dirname(__file__)
    root = dirname + "//" + "static//temp//home//pi//data"
    pattern = "*.jpg"
    print(root)
    intcounter = 0
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                arraytime = name.split('-')
                if len(arraytime) == 1:
                    name = name + "-video1"
                timestamp = name.split('-')[0]
                timestamp = timestamp.split(".jpg")[0]
                # print(timestamp)
                dt_obj = datetime.fromtimestamp(float(timestamp)).time().strftime("%H:%M")
                allfilenamesindatetime.append(timestamp)
                timeinstr = dt_obj
                # print(dt_obj)
                if name.split('-')[1] not in videonums:
                    data.append(dt_obj)
                    videonums.append(name.split('-')[1])
                '''mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="Emma150799!",
                    database="testdb"
                )
                mycursor = mydb.cursor()'''
                intcounter = intcounter + 1
        # mycursor.execute("CREATE TABLE videos (title VARCHAR(255) PRIMARY KEY, url VARCHAR(255), timecreated DATETIME(6), durationinseconds INT(255))")
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

        # for i in range(0,len(zippedfilenames)):
        # print(zippedfilenames[i])
        # str = zippedfilenames[i]
        # timestr = str.split(' ')
        # day = timestr[0].split('-')[0];
        # month = timestr[0].split('-')[1];
        # year = timestr[0].split('-')[2];
        # hour = timestr[1].split('.')[0];
        # minute = timestr[1].split('.')[1];
        # seconds = timestr[1].split('.')[2];
        # mtime = creationdate(zippedfilenames[i])
        # print(mtime)


@app.route('/')
def index():
    # data = ["4:00 AM","4:00 AM","4:00 AM","4:00 AM","4:00 AM"]
    dirname = os.path.dirname(__file__)
    value = dirname + "\\" + 'temp/7.05-video1.jpg'
    # imagedata = [url_for('static', filename='temp/7.05-video1.jpg'),url_for('static', filename='temp/7.05-video1.jpg'),url_for('static', filename='temp/7.05-video1.jpg')]
    return render_template('index.html', data=data, imagedata=imagedata)


@app.route('/my-link/')
def my_link():
    print('I got clicked!')
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global staticcurrentvideotime
    global imagedata
    global imagedatacopy
    print(request.form)
    if "time" in request.form:
        print(request.form)
        print(request.form.getlist("time"))
        for filename in allfilenamesindatetime:
            filenameinhourandminute=datetime.fromtimestamp(float(filename)).time().strftime("%H:%M")
            staticcurrentvideotime = filenameinhourandminute
            if(filenameinhourandminute==request.form.getlist("time")[0]):                
                stringfilename = 'temp/home/pi/data/'+str(filename)+'.jpg'
                imagedata.append(url_for('static', filename=stringfilename))
                imagedatacopy.append(url_for('static', filename=stringfilename))
        print(len(imagedata))
        return redirect(request.url)
    elif "delete" in request.form:
        if request.method== 'POST':
            print(staticcurrentvideotime)
            print("checked")
            print(len(imagedata))
            #valuearray = request.form.getlist("images")
            #valuearray = imagedata
            dirname = os.path.dirname(__file__)
            for value in imagedatacopy:
                #print(value)
                value1 = value
                #print(value1)
                value1 = value1.replace("/","\\")
                value1= dirname +"\\"+ value1                
                value1 = value1.replace("\\\\","\\")
                #print(dirname)
                #print(value1)
                if os.path.exists(value1):
                    #print("deleted")
                    os.remove(value1)
                    imagedata.remove(value)
                else:
                    print("path not found")
                imagedatacopy = imagedata
            data.remove(staticcurrentvideotime)
            return redirect(request.url)
    elif request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
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
            print(url_for('upload_file',
                          filename=filename))
            file_upload(file)
            return redirect(url_for('upload_file', filename=filename))
    return


if __name__ == '__main__':
    app.run(debug=False)

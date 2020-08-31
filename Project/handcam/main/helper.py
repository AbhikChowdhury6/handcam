from __future__ import print_function
import argparse
import contextlib
from datetime import datetime
import shutil
import os
import six
import sys
import json
import time
import unicodedata
import zipfile
import platform
from fnmatch import fnmatch
from subprocess import check_output, CalledProcessError, STDOUT
from flask import current_app as curr_app
from flask import Flask, render_template, request, redirect, url_for, Blueprint,flash
from werkzeug.utils import secure_filename
from distutils.dir_util import copy_tree

def file_upload(folderPath, pathfile,current_user):
    pathfilename = secure_filename(pathfile.filename)
    finalFileName = pathfilename.split(".")[0]
    root = folderPath +"/"+finalFileName
    zipPath = zipfile.ZipFile(pathfile, 'r')

    print("Root: " + root)
    if not os.path.exists(root + "/data"):
        os.makedirs(root + "/data")

    if not os.path.exists(root + "/tmp"):
        os.makedirs(root + "/tmp")
    
    zipFileList = zipPath.namelist()
    for value in zipFileList:
        tval = value.split("/")
        tval = tval[len(tval)-1]
        if (value.endswith('.csv') or value.endswith('.jpg')) and (tval.startswith("._")!=True):
           zipPath.extract(value, root + "/tmp")
           shutil.move(root+"/tmp/"+value,root + "/data/"+value.split("/")[-1])
    shutil.rmtree(root+"/tmp")

    timeFrame = {}
    videonums = {}
    pattern = "*.jpg"

    finalResult = {}
    filePath = 'collectedData/'+ current_user +"/"+ finalFileName +'/rotated_images/'
    for path, dir, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                if name[0] != ".":
                    print("Filename: " +  str(name))
                    timestamp = name.split('-')[0]
                    print("Timestamp : " + str(timestamp))
                    dt_obj = datetime.fromtimestamp(float(timestamp)).time().strftime("%H:%M")
                    print(dt_obj)
                    frameNo = ((name.split('-')[1]).split('.')[0])
                    if frameNo not in videonums:
                        videonums[frameNo] = []
                        timeFrame[frameNo] = dt_obj
                        videonums[frameNo].append(filePath + name)
                    else:
                        videonums[frameNo].append(filePath + name)

    finalResult['videoNum'] = videonums
    finalResult['timeFrame'] = timeFrame
    return finalResult
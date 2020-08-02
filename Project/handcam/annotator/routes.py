from flask import Flask,render_template, request, Blueprint,flash,redirect,url_for
from handcam.models import rigDeviceData
from handcam.extensions import db
from flask_login import current_user, login_required
from flask import current_app as curr_app
from werkzeug.utils import secure_filename
import os,errno,json
import pandas as pd
from datetime import datetime
annotator = Blueprint('annotator', __name__)

global result

@annotator.route("/annHome",methods=['GET','POST'])
@login_required
def home():
	if current_user.is_authenticated and current_user.isAnnotator==1:
		rigData = rigDeviceData.query.all()
		print(rigData)
		return render_template('annotator/home-ann.html',rigData=rigData,user=current_user)

@annotator.route("/round3/<fileId>", methods=['GET','POST'])
@login_required
def roundThree(fileId):
	if current_user.is_authenticated and current_user.isAnnotator==1:
		# imagedata = []
		# timedata = []
		rigValue =  rigDeviceData.query.filter_by(id=fileId).first_or_404()
		# print(rigValue)
		result = json.loads(rigValue.fileContent)
		timedata = result['timeFrame']
		print("Round 3 display code is running...")
		fresult = timeFrameData(timedata)
		filePath = curr_app.root_path + (rigValue.filePath).split(".zip")[0] + "/updated_csv/afterRound1.csv"
		if not os.path.exists(filePath):
			flash(" No filePath for fetching isgrasping exists")
			return render_template('annotator/round3.html',title='Round 3',fileId = fileId, timedata = fresult)
		else:
			pdValues = pd.read_csv(filePath)
			row = pdValues.index[pdValues['isGrasping'] == 1]
			length = len(row)
			print(length)
			return render_template('annotator/round3.html',title='Round 3',fileId = fileId, timedata = fresult,isgrasping=length)
		# flash('Click on time frame to get the data','info')
		return render_template('annotator/round3.html',title='Round 3',fileId = fileId, timedata = fresult)
	else:
		return redirect(url_for('users.login'))

@annotator.route("/round3Data/<fileId>", methods=['GET','POST'])
@login_required
def roundThreeData(fileId):
	print("RoundThree data code is running...")
	if current_user.is_authenticated and current_user.isAnnotator==1:
		if request.method == 'POST':
			formTime = request.form['time']
			print(formTime)
			timeSelected = formTime.split('(')[0]
			timeFrame = (formTime.split('(')[1]).split(')')[0]
			imagedata = []
			timedata = []
			rigValue =  rigDeviceData.query.filter_by(id=fileId).first_or_404()
			# print(rigValue)
			result = json.loads(rigValue.fileContent)
			timedata = result['timeFrame']
			imagedata = result['videoNum'][timeFrame]
			fresult = timeFrameData(timedata)
			return render_template('annotator/round3.html',title='round3', fileId = fileId, timedata = fresult, imagedata = imagedata)
		else:
			imagedata = []
			timedata = []
			rigValue =  rigDeviceData.query.filter_by(id=fileId).first_or_404()
			print(rigValue)
			result = json.loads(rigValue.fileContent)
			timedata = result['timeFrame']
			print("Round 1 display code is running...")
			fresult = timeFrameData(timedata)
			return render_template('annotator/round3.html',title='round3',fileId = fileId, timedata = fresult)
	else:
		return redirect(url_for('users.login'))

def timeFrameData(timedata):
	tnums = sorted(timedata.keys())
	fresult = {}
	for value in tnums:
		fresult[value] = timedata[value]
	return fresult
from flask import Flask,render_template, request, Blueprint,flash,redirect,url_for
from handcam.models import rigDeviceData
from handcam.extensions import db
from flask_login import current_user, login_required
from flask import current_app as curr_app
from werkzeug.utils import secure_filename
import os,errno,json
from datetime import datetime
from handcam.main.helper import file_upload
from handcam.main.imageStabilization import apply_imageStabilization
from handcam.main.thresholdAlgorithm import apply_thresholdAlgo
from handcam.main.csvAddition import AddingtoCSV
main = Blueprint('main', __name__)

global result

@main.route("/",methods=['GET','POST'])
@login_required
def home():
	if current_user.is_authenticated:
		rigData = rigDeviceData.query.filter_by(user_id=current_user.id).order_by(rigDeviceData.uploaded_at.desc())
	return render_template('home.html',rigData=rigData,user=current_user)

@main.route("/upload", methods=['GET','POST'])
@login_required
def upload():
	global result
	if current_user.is_authenticated:
		if request.method == 'POST':

			if 'file' not in request.files:
				flash('No file part in the request ','danger')
				return render_template('upload.html', title='Upload')

			file = request.files['file']
			if file.filename == '':
				flash('No file selected.','danger')
				return render_template('upload.html', title='Upload')

			if file:
				filename = secure_filename(file.filename)
				savePath = curr_app.root_path + "/static/collectedData/" + str(current_user.id)
				
				if not os.path.exists(savePath):
					os.makedirs(savePath)

				flag = False
				filePath = savePath + "/" + filename

				if os.path.exists(filePath):
					flag = False
				else:
					file.save(savePath + "/" + filename)
					finalResult = file_upload(savePath,file,str(current_user.id))
					
					print("Printing the result after return call from helper file")
					#print(result)
					filePath = "/static/collectedData/"+str(current_user.id) + "/" + filename
					flag = True

				if(flag == False):
					print("Uploaded file with same folder already exists.")
					flash('Uploaded file with same folder name already exists.','info')
					return render_template('upload.html', title='Upload')
				else:
					rigData = rigDeviceData(filename=filename, filePath= str(filePath), fileContent=json.dumps(finalResult),user_id=current_user.id)
					db.session.add(rigData)
					db.session.commit()
					print("File uploaded successfully")
					flash('File uploaded successfully.','success')
					return redirect(url_for('main.roundOne',fileId = rigData.id))
		else:
			return render_template('upload.html', title='Upload')
	else:
		return redirect(url_for('users.login'))

@main.route("/round1/<fileId>", methods=['GET','POST'])
@login_required
def roundOne(fileId):
	if current_user.is_authenticated:
		imagedata = []
		timedata = []
		rigValue =  rigDeviceData.query.filter_by(id=fileId,user_id=current_user.id).first_or_404()
		print(rigValue)
		result = json.loads(rigValue.fileContent)
		timedata = result['timeFrame']
		print("Round 1 display code is running...")
		fresult = timeFrameData(timedata)
		flash('Click on time frame to get the data','info')
		return render_template('roundOne.html',title='roundOne',fileId = fileId, timedata = fresult)
	else:
		return redirect(url_for('users.login'))

@main.route("/round1Data/<fileId>", methods=['GET','POST'])
@login_required
def roundOneData(fileId):
	print("RoundOne data code is running...")
	if current_user.is_authenticated:
		if request.method == 'POST':
			formTime = request.form['time']
			print(formTime)
			timeSelected = formTime.split('(')[0]
			timeFrame = (formTime.split('(')[1]).split(')')[0]
			imagedata = []
			timedata = []
			rigValue =  rigDeviceData.query.filter_by(id=fileId,user_id=current_user.id).first_or_404()
			# print(rigValue)
			result = json.loads(rigValue.fileContent)
			timedata = result['timeFrame']
			imagedata = result['videoNum'][timeFrame]
			fresult = timeFrameData(timedata)
			return render_template('roundOne.html',title='roundOne', fileId = fileId, timedata = fresult, imagedata = imagedata)
		else:
			imagedata = []
			timedata = []
			rigValue =  rigDeviceData.query.filter_by(id=fileId,user_id=current_user.id).first_or_404()
			print(rigValue)
			result = json.loads(rigValue.fileContent)
			timedata = result['timeFrame']
			print("Round 1 display code is running...")
			fresult = timeFrameData(timedata)
			return render_template('roundOne.html',title='roundOne',fileId = fileId, timedata = fresult)
	else:
		return redirect(url_for('users.login'))

@main.route("/round1Delete/<fileId>", methods=['GET', 'POST'])
@login_required
def roundOneDelete(fileId):
	print("Delete button is pressed.")
	if current_user.is_authenticated:
		if request.method == 'POST':
			data = request.json['frameNo']

			rigValue =  rigDeviceData.query.filter_by(id=fileId,user_id=current_user.id).first_or_404()
			result = json.loads(rigValue.fileContent)
			timedata = result['timeFrame']
			imagedata = result['videoNum']

			if data in timedata :
				del timedata[data]
			else:
				return json.dumps({'fileId':rigValue.id,'flag':'error'})

			if data in imagedata :
				for value in imagedata[data]:
					path = curr_app.root_path + '/static/' + value
					if os.path.exists(path):
						os.remove(path)
				del imagedata[data]
			else:
				return json.dumps({'fileId':rigValue.id,'flag':'error'})

			rigValue.fileContent = json.dumps({'timeFrame': timedata, 'videoNum' : imagedata})
			rigValue.id = rigValue.id
			db.session.add(rigValue)
			db.session.commit()
			
			fresult = timeFrameData(timedata)
			imagedata = []
			#return redirect(url_for('main.roundOne',fileId = rigData.id))
			return json.dumps({'fileId':rigValue.id,'flag':'success'})
			
	else:
		return redirect(url_for('users.login'))

@main.route("/round1Submit/<fileId>", methods=['GET', 'POST'])
@login_required
def roundOneSubmit(fileId):
	if current_user.is_authenticated:
		if request.method == 'POST':
			data = (request.json['tagData'])
			print(data)
			
			rigValue =  rigDeviceData.query.filter_by(id=fileId,user_id=current_user.id).first_or_404()
			filePath = curr_app.root_path + (rigValue.filePath).split(".zip")[0]
			apply_imageStabilization(filePath)
			apply_thresholdAlgo( filePath)
			AddingtoCSV( filePath, data)
			return json.dumps({'fileId':fileId,'flag':'success'})
			
	else:
		return redirect(url_for('users.login'))

def timeFrameData(timedata):
	tnums = sorted(timedata.keys())
	fresult = {}
	for value in tnums:
		fresult[value] = timedata[value]
	return fresult



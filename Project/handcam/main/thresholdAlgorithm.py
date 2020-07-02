import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, peak_prominences
from flask import current_app as curr_app

def apply_thresholdAlgo( filePath):
    # print("Threshold function started")
	csvPath = filePath + "/updated_csv"
	v4_data=pd.read_csv( csvPath + "/merged_handled.csv")
	# v4_data=pd.read_csv("/merged_handled.csv")

	v4_data['ax_ma']=v4_data.ax.rolling(window=20,min_periods=1).mean()
	v4_data['ay_ma']=v4_data.ay.rolling(window=20,min_periods=1).mean()
	v4_data['az_ma']=v4_data.az.rolling(window=20,min_periods=1).mean()

	# threosholding technique
	v4_data_preprocessed=v4_data.iloc[:,11:14]

	array=v4_data_preprocessed.values

	v4_data_test=v4_data[['ax_ma','ay_ma','az_ma']] #alternative to iloc

	v4_data['normalized']=np.linalg.norm(v4_data_test.values,axis=1)

	#removing gravity contribution
	v4_data['normalizedG']=v4_data['normalized']-1

	possible_t3,_=find_peaks(v4_data.normalizedG, distance=100,prominence=0.05,width=(None,30))

	imu_grasping_index=v4_data.normalizedG[possible_t3]

	v4_data['isGrasping']=0 # initialize a new column with all zero values
	v4_data.iat[904,16]=1
	v4_data.iat[2814,16]=1

	#saving the final file
	v4_data.to_csv( csvPath + "/final.csv") 
	# v4_data.to_csv( '/final.csv') 
	print("Final csv file is generated successfully")

# apply_thresholdAlgo()
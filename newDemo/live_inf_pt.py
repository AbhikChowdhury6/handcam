import numpy as np
import matplotlib.pyplot as plt

G_PHX = 9.802
INF_LEN = 3
pre_conv_kernel = 7
post_conv_kernel = 3

buffer_len = INF_LEN*2 + pre_conv_kernel + post_conv_kernel - 2

folder = 'trial12'
accel = 'trial12-BNO05500-ACCEL-24-06-2019-22-33-34.1561412014454.csv'
grav = 'trial12-BNO05500-GRAV-24-06-2019-22-33-34.1561412014454.csv'
gyro = 'trial12-BNO05500-GYRO-24-06-2019-22-33-34.1561412014454.csv'

#manual experimentation gave mask of 100 for accel and grav, 10 for gyro

def load_and_proc(filepath, mask = 100):
	rawtext = open(filepath, "r").readlines()[0]
	split = rawtext.split("(")
	out_data = []
	for dp in split:
		if dp == '':
			continue
		dp_split = dp[:-2].split(",")
		out_list = [float(numf) for numf in dp_split]
		out_data.append(np.array(out_list))
	out_data = np.stack(out_data)
	masked = np.abs(out_data) < mask
	return masked * out_data

def lowpass(data, kernel_size = 50, channels = 3):
	kernel = np.ones(kernel_size) / kernel_size
	convolved = []
	if channels > 1:
		for channel in range(channels):
			convolved.append(np.convolve(data[:,channel],kernel,'valid'))
	else:
		convolved = [np.convolve(data,kernel,'valid')]
	return np.transpose(np.stack(convolved))

def interp_grav(data):
	grav_mag = np.sqrt(np.sum(data*data,axis=1))
	outliers = np.where(np.abs(grav_mag - G_PHX) > 0.01) [0]
	#init_errs = np.where(grav_mag == 0)
	data[outliers] = (data[outliers-1] + data[outliers+1]) / 2
	#data[init_errs] = data[np.max(init_errs)+1]
	return data

def lpf_plot(data, kernel_size, ax):
	datalp = lowpass(data,kernel_size)
	ax.plot([0,datalp.shape[0]],[0,0],'k')	
	ax.plot(datalp[:,0],c='#111111')
	ax.plot(datalp[:,1],c='#555555')
	ax.plot(datalp[:,2],c='#999999')

def find_inf_pt(accel, gyro, eps = 0.001):
	accel_mag = lowpass(np.sqrt(np.sum(accel*accel,axis=1)),post_conv_kernel,1)
	gyro_mag = lowpass(np.sqrt(np.sum(gyro*gyro,axis=1)),post_conv_kernel,1)
	#inf_pt = np.logical_or(accel_mag < eps, gyro_mag < eps)
	inf_pt = 1 * (accel_mag < eps)
	pos_sl = np.sum(inf_pt[-INF_LEN:]) > INF_LEN/2 and np.sum(inf_pt[-INF_LEN:-INF_LEN]) < INF_LEN/2
	neg_sl = np.sum(inf_pt[-INF_LEN:]) < INF_LEN/2 and np.sum(inf_pt[-INF_LEN:-INF_LEN]) > INF_LEN/2
	return pos_sl or neg_sl

def get_data():
	return 1

datastreaming = True
acdl = []
gydl = []
while datastreaming:
	#new_acd, new_gyr = get_data()
	if len(new_acd) <= buffer_len:
		acdl.append(new_acd)
		gydl.append(new_gyr)
	else:
		acdl = acd[1:] + [new_acd]
		gydl = gyr[1:] + [new_acd]
	acd = np.ndarray(acdl)
	gyd = np.ndarray(gydl)
	lpac = lowpass(acd-grd, pre_conv_kernel)
	lpgy = lowpass(gyd, pre_conv_kernel)
	ip = find_inf_pt(lpac, lpgy, eps=0.3)
	if ip:
		#send_camera_image()























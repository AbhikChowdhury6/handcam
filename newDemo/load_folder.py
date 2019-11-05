import numpy as np
import matplotlib.pyplot as plt

G_PHX = 9.802

pre_conv_kernel = 7
post_conv_kernel = 3

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
			convolved.append(np.convolve(data[:,channel],kernel,'same'))
	else:
		convolved = [np.convolve(data,kernel,'same')]
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
	inf_pt_ac = np.logical_and(accel_mag < eps, gyro_mag >= eps)
	inf_pt_gy = np.logical_and(accel_mag < eps, gyro_mag < eps)
	return np.where(inf_pt_ac)[0], np.where(inf_pt_gy)[0], accel_mag, gyro_mag

acd = load_and_proc(folder + '/' + accel)
grd = interp_grav(load_and_proc(folder + '/' + grav))
gyd = load_and_proc(folder + '/' + gyro, 10)

print(acd.shape)
print(grd.shape)
print(gyd.shape)

'''plt.plot(acd[:,0])
plt.plot(acd[:,1])
plt.plot(acd[:,2])
plt.show()
'''
#no filtering
eps = 0.3
kernel_size = pre_conv_kernel
lpac = lowpass(acd-grd, kernel_size)
lpgy = lowpass(gyd,kernel_size)
lpgr = lowpass(grd,kernel_size)
infpta, infptg, accel_mag, gyro_mag = find_inf_pt(lpac,lpgy,eps)
'''fig, (ax1,ax2,ax3) = plt.subplots(3)
lpf_plot(acd[-500:]-grd[-500:], kernel_size, ax1)
lpf_plot(grd[-500:], kernel_size, ax2)
lpf_plot(gyd[-500:], kernel_size, ax3)
plt.plot()
plt.show()	'''
#fig, (ax1) = plt.subplots(2)
z_thresh = np.log(eps)
plt.plot([0,accel_mag.shape[0]],[z_thresh,z_thresh],'k')	
plt.plot(np.log(gyro_mag),c='#999999')
plt.plot(np.log(accel_mag),c='#111111')
#lpf_plot(lpgy[2:2000],1,ax2)
plt.scatter(infpta,np.ones(infpta.shape)*z_thresh,marker="|",zorder=9,c="r",s=1000)
plt.scatter(infptg,np.ones(infptg.shape)*z_thresh,marker="|",zorder=9,c="b",s=1000)	
#ax2.scatter(infpt,np.zeros(infpt.shape),marker="|",zorder=9,c="r",s=1000)
plt.show()
import time
import adafruit_bno055

class BNO0551:
	def __init__(self, i2c, path):
		self.address = 0x29
		self.REFRESH_RATE = 1
		self.i2c = i2c
		self.name = "BNO05501"
		self.DATA_PATH = path
		self.sensor = adafruit_bno055.BNO055(i2c, self.address)

		millis = int(round(time.time() * 1000))
		self.ACCEL_f = open(self.DATA_PATH + "-" + self.name + "-ACCEL-" + time.strftime('%d-%m-%Y-%H-%M-%S', time.localtime()) + "." + str(millis) + ".csv", "a+")
		self.GYRO_f = open(self.DATA_PATH + "-" + self.name + "-GYRO-" + time.strftime('%d-%m-%Y-%H-%M-%S', time.localtime()) + "." + str(millis) + ".csv", "a+")
		self.MAG_f = open(self.DATA_PATH + "-" + self.name + "-MAG-" + time.strftime('%d-%m-%Y-%H-%M-%S', time.localtime()) + "." + str(millis) + ".csv", "a+")
		self.EULERA_f = open(self.DATA_PATH + "-" + self.name + "-EULERA-" + time.strftime('%d-%m-%Y-%H-%M-%S', time.localtime()) + "." + str(millis) + ".csv", "a+")
		self.QUATER_f = open(self.DATA_PATH + "-" + self.name + "-QUATER-" + time.strftime('%d-%m-%Y-%H-%M-%S', time.localtime()) + "." + str(millis) + ".csv", "a+")
		self.LINACCEL_f = open(self.DATA_PATH + "-" + self.name + "-LINACCEL-" + time.strftime('%d-%m-%Y-%H-%M-%S', time.localtime()) + "." + str(millis) + ".csv", "a+")
		self.GRAV_f = open(self.DATA_PATH + "-" + self.name + "-GRAV-" + time.strftime('%d-%m-%Y-%H-%M-%S', time.localtime()) + "." + str(millis) + ".csv", "a+")



	def log(self):
		self.ACCEL_f.write(str(self.sensor.accelerometer) + ",")
		self.GYRO_f.write(str(self.sensor.gyroscope) + ",")
		self.MAG_f.write(str(self.sensor.magnetometer) + ",")
		self.EULERA_f.write(str(self.sensor.euler) + ",")
		self.QUATER_f.write(str(self.sensor.quaternion) + ",")
		self.LINACCEL_f.write(str(self.sensor.linear_acceleration) + ",")
		self.GRAV_f.write(str(self.sensor.gravity) + ",")

		return True

	def end(self):
		self.ACCEL_f.close()
		self.GYRO_f.close()
		self.MAG_f.close()
		self.EULERA_f.close()
		self.QUATER_f.close()
		self.LINACCEL_f.close()
		self.GRAV_f.close()


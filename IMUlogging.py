# thisfile is to grab all of the data on the i2c bus based on the the configuration file
#write it to files
# keep an open socket and stream it (via jttp https later)
import time
import smbus
import os

#import all of the devices on the bus for now
from i2cMPU60500 import MPU60500
bus = smbus.SMBus(1)

#defince product name
PRODUCT_NAME ="handcam"
DATA_PATH="TEST"


# extanciate and configure all of the objects
mpu60500 = MPU60500(bus, DATA_PATH)


print time.strftime('%d-%m-%Y-%H-%M-%S', time.localtime())
divider = 1
second = 0
starttime=time.time()
while True:

  if (divider % mpu60500.REFRESH_RATE == 0):
      mpu60500.log(bus)

  divider = divider + 1
  time.sleep(0.01 - ((time.time() - starttime) % 0.01))


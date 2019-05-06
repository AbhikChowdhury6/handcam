# thisfile is to grab all of the data on the i2c bus based on the the configuration file
#write it to files
# keep an open socket and stream it (via jttp https later)
import time
import os
import sys
from busio import I2C
from board import SDA, SCL


#import all of the devices on the bus for now
from i2cBNO0550 import BNO0550

i2c = I2C(SCL, SDA)

#defince product name
PRODUCT_NAME = "*"
DATA_PATH = sys.argv[1]


# extanciate and configure all of the objects
bno0550 = BNO0550(i2c, DATA_PATH)


print (time.strftime('%d-%m-%Y-%H-%M-%S', time.localtime()))
divider = 1
second = 0
starttime=time.time()
while True:

  if (divider % bno0550.REFRESH_RATE == 0):
      bno0550.log()


  divider = divider + 1
  time.sleep(0.01 - ((time.time() - starttime) % 0.01))


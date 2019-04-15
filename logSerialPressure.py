import serial
import time
import sys

#comPort = sys.argv[1]
comPort = "/dev/ttyUSB0"
arduinoData = serial.Serial(comPort, 115200) #Creating our serial object named arduinoData

PRESS_f = open( sys.argv[1] + "-" + "PARRAY3" + "-PRESS-" + time.strftime('%d-%m-%Y-%H-%M-%S', time.localtime()) + "." + str(int(round(time.time() * 1000))) + ".csv", "a+")

while True:
    while (arduinoData.inWaiting()==0): #Wait here until there is data
        pass #do nothing
    arduinoString = arduinoData.readline() #read the line of text from the serial port
    PRESS_f.write(arduinoString + ",")
    
PRESS_f.close()
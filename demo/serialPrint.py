import serial
import time



comPort = "/dev/ttyUSB0"
arduinoData = serial.Serial(comPort, 115200) #Creating our serial object named arduinoData
while True:
    while (arduinoData.inWaiting()==0): #Wait here until there is data
        pass #do nothing
    arduinoString = arduinoData.readline() #read the line of text from the serial port
    
    dat = str(time.time()) + "," + str(arduinoString)
    print(dat)
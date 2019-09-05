import websocket
import serial
import time
import sys


serverAddr = sys.argv[1]
subSample = int(sys.argv[2])

ws = websocket.create_connection("ws://" + serverAddr + ":9001")

comPort = "/dev/ttyUSB0"
arduinoData = serial.Serial(comPort, 115200) #Creating our serial object named arduinoData

count = 0

while True: 
    while (arduinoData.inWaiting()==0): #Wait here until there is data
        pass #do nothing
    arduinoString = arduinoData.readline() #read the line of text from the serial port
    
    dat = str(time.time()) + "," + str(arduinoString)
    if (count == subSample):
        count = 0
        print(dat)
        ws.send(dat)

    count = count + 1


ws.close()
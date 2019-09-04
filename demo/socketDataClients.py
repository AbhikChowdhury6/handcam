# WS client example

import asyncio
import websockets
import sys
import serial
import time

targetAddr = sys.argv[1]

comPort = "/dev/ttyUSB0"
arduinoData = serial.Serial(comPort, 115200) #Creating our serial object named arduinoData

async def sendDataContinually(data):
    uri = "ws://" + targetAddr + ":8765"
    async with websockets.connect(uri) as websocket:
        while True:
            while (arduinoData.inWaiting()==0): #Wait here until there is data
                pass #do nothing
            arduinoString = arduinoData.readline() #read the line of text from the serial port
            
            dat = str(time.time()) + "," + str(arduinoString)
            await websocket.send(dat)
            print(f"> {dat}")

            response = await websocket.recv()
            print(f"< {response}")

asyncio.get_event_loop().run_forever(sendDataContinually())
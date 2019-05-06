import serial
import numpy
import matplotlib.pyplot as plt
import sys
#from drawnow import *


#usage
## first arg is the port
#additional args are the names of streams

numStreams = len(sys.argv) - 2
print(numStreams)
comPort = sys.argv[1]

datatypes = []
values = []

for i in range(numStreams):
    datatypes.append(sys.argv[i+2])
    values.append([])





arduinoData = serial.Serial(comPort, 115200) #Creating our serial object named arduinoData
plt.ion() #Tell matplotlib you want interactive mode to plot live data
cnt=0

def makeFig(data, title, xlabel): #Create a function that makes our desired plot
    plt.ylim(0,512)                                 #Set y min and max values
    plt.title(title)      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel(title)                            #Set ylabels
    plt.xlabel(xlabel)                            #Set ylabels
    plt.plot(data, 'ro-', label=title)       #plot the temperature
    plt.legend(loc='upper left')                    #plot the legend
    plt.draw()
    plt.pause(0.001)

    
plt.figure()

for i in range(numStreams):
        plt.subplot(numStreams,1,i+1)

        #plt.ylim(0,512)                                 #Set y min and max values
        plt.title(datatypes[i])      #Plot the title
        plt.grid(True)                                  #Turn the grid on
        plt.ylabel(datatypes[i])                            #Set ylabels
        plt.xlabel('samples')                            #Set ylabels
        plt.plot(values[i], 'ro-', label=datatypes[i])       #plot the temperature
        plt.legend(loc='upper left')                    #plot the legend

while True: # While loop that loops forever
    arduinoData.flushInput()
    while (arduinoData.inWaiting()==0): #Wait here until there is data
        pass #do nothing
    arduinoString = arduinoData.readline() #read the line of text from the serial port
    subStr = ""
    dataArray = arduinoString[1:-3].split(",")   #Split it into an array called dataArray
    
    for i in range(numStreams):
        print(dataArray[i])
        values[i].append(float(dataArray[i]))
    #plt.clf()
    for i in range(numStreams):
        plt.subplot(numStreams,1,i+1)
        plt.cla()
        plt.plot(values[i], 'ro-', label=datatypes[i])
        plt.draw()
        plt.pause(0.001)

        #makeFig(values[i],datatypes[i],'samples')
        #drawnow(makeFig(values[i],datatypes[i],'samples'))    #Call drawnow to update our live graph
        #plt.pause(.000001)                     #Pause Briefly. Important to keep drawnow from crashing
    
    cnt=cnt+1
    if(cnt>50):                            #If you have 50 or more points, delete the first one from the array
        for i in range(numStreams):
            values[i].pop(0)
import websocket
import sys
import numpy
import matplotlib.pyplot as plt


serverAddr = sys.argv[1]
title = sys.argv[2]
dataIndex = sys.argv[3]

ws = websocket.create_connection("ws://" + serverAddr + ":9001")


plt.ion() #Tell matplotlib you want interactive mode to plot live data

values = []

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


plt.ylim(0,512)                                 #Set y min and max values
plt.title(title)      #Plot the title
plt.grid(True)                                  #Turn the grid on
plt.ylabel(title)                            #Set ylabels
plt.xlabel('samples')                            #Set ylabels
plt.plot(values[i], 'ro-', label=datatypes[i])       #plot the temperature
plt.legend(loc='upper left')                    #plot the legend

cnt = 0
while True:
    result =  ws.recv()

    packetList = result.split('(')   #Split it into an array called dataArray
    print(packetList)
    dataList = packetList[1].split(',')
    
    values.append(dataIndex[0])

    plt.cla()
    plt.plot(values[i], 'ro-', label=datatypes[i])
    plt.draw()
    plt.pause(0.001)

    cnt=cnt+1
    if(cnt>50):                            #If you have 50 or more points, delete the first one from the array
        for i in range(numStreams):
            values[i].pop(0)
    
    
ws.close()
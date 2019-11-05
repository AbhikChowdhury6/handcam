import websocket
import sys
import numpy
import matplotlib.pyplot as plt


serverAddr = sys.argv[1]
dataIndex = int(sys.argv[2])
title = sys.argv[3]

ws = websocket.create_connection("ws://" + serverAddr + ":9001")


plt.ion() #Tell matplotlib you want interactive mode to plot live data

values = []


cnt = 0
while True:
    result =  ws.recv()
    packetList = result.split('(')   #Split it into an array called dataArray
    dataList = packetList[1].split(',')
    
    values.append(float(dataList[dataIndex]))
    #print(values)
    plt.cla()

    plt.title(title)      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel(title)                            #Set ylabels
    plt.plot(range(0,len(values)), values , 'ro-', label=title)     
    
    plt.draw()
    plt.pause(0.001)

    cnt=cnt+1
    if(cnt>50):                            #If you have 50 or more points, delete the first one from the array
        values.pop(0)
    
    
ws.close()
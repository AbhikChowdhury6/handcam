import asyncio
import websockets
import numpy
import matplotlib.pyplot as plt


plt.ion() #Tell matplotlib you want interactive mode to plot live data


ok = "OK"

numStreams = 6
datatypes = ["Accel X", "Accel Y", "Accel Z", "P1", "P2", "P3"]
values = [[],[],[],[],[],[]]
lastVal = ""

async def dataCap(websocket, path):
    dat = await websocket.recv()
    print(f"< {dat}")
    lastVal = dat
    #buffer.append()

    await websocket.send(ok)
    print(f"> {ok}")

start_server = websockets.serve(dataCap, "", 8765)

asyncio.get_event_loop().run_until_complete()
asyncio.get_event_loop().run_forever(start_server)

cnt=0

print("I am here!")

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
    
    subStr = ""
    dataArray = lastVal.split(",")   #Split it into an array called dataArray
    
    #parse pressure
    #parse accel
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


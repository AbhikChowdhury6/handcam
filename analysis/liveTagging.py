import time
import sys
#read in input and log to a file the type of experment, trial name the timestamp
TAGS_F = open( sys.argv[1] + "tags.csv", "a+")

EXP = [0,0,0,0,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3]
OBJ = ["c", "k","t", "m", "c","p","s","c","p","s","k","t","m","c","p","s","k","t","m"] 

output = []

i = 0

while True:
    if i == len(EXP):
        break
    experementType = EXP[i] # input("enter experement type ")
    objectType = OBJ[i]# input("enter object type ")
    print(experementType)
    print(objectType)
    
    inp = input("press enter to indicate the start time or b to redo last experement")
    if inp == 'b':
        _ = output.pop()
        i = i - 1
        continue

    startTime = time.strftime('%d-%m-%Y-%H-%M-%S', time.localtime()) + "." + str(round(time.time() * 1000))

    _ = input("press enter when complete")
    endTime = time.strftime('%d-%m-%Y-%H-%M-%S', time.localtime()) + "." + str(round(time.time() * 1000))

    print("added :" + "(" + str(experementType) + "," + str(objectType) + "," + startTime + "," + endTime + "),")
    output.append("(" + str(experementType) + "," + str(objectType) + "," + startTime + "," + endTime + "),")

    i = i + 1


for o in output:
    TAGS_F.write(o)
 
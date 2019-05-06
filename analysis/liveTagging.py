import time

#read in input and log to a file the type of experment, trial name the timestamp
TAGS_F = open( "tags.csv", "a+")

EXP = [1,1,1,2,2,2,2,2,2,3,3,3,3,3,3]
OBJ = ["c","p","s","c","p","s","k","t","m","c","p","s","k","t","m"]

i = 0

while True:

    experementType = EXP[i] # input("enter experement type ")
    objectType = OBJ[i]# input("enter object type ")
    print(experementType)
    print(objectType)
    
    i = i + 1
    inp = input("press enter to indicate the start time or e to manually enter experement and object type")
    if inp == 'e':
        experementType = input("enter experement type ")
        objectType = input("enter object type ")
        _ = input("press enter to indicate the start time")

    startTime = time.strftime('%d-%m-%Y-%H-%M-%S', time.localtime()) + "." + str(round(time.time() * 1000))

    _ = input("press enter when complete")
    endTime = time.strftime('%d-%m-%Y-%H-%M-%S', time.localtime()) + "." + str(round(time.time() * 1000))

    print("added :" + "(" + str(experementType) + "," + str(objectType) + "," + startTime + "," + endTime + "),")
    TAGS_F.write("(" + str(experementType) + "," + str(objectType) + "," + startTime + "," + endTime + "),")
 
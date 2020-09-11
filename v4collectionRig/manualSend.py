import os
import time
import sys

#example "chowder@192.168.0.100:"
target = sys.argv[1]

#make all files if theyre not already there
os.system("mkdir /home/pi/export && mkdir /home/pi/export2 && /home/pi/export3")

#move old export2 file to export3 and delete
os.system("rm /home/pi/export3/* && mv /home/pi/export2/* /home/pi/export3/")

#move old export file to export2 for safe keeping
os.system("mv /home/pi/export/* /home/pi/export2")
        
#move the data folder to export and make a new data folder for next time
t = str(time.time()).split(".")
t[1] = t[1] + "000"
os.system("cd /home/pi/ && zip -r /home/pi/export/" + t[0] + "." + t[1][:3] + ".zip data")

#remove items in the data folder
os.system("rm -r /home/pi/data/ && mkdir /home/pi/data")

os.system("scp /home/pi/export/* " + target)

#reset recording number to zero
vidNF = open( "/home/pi/vidnum.txt", "w")
vidNF.write("0")
vidNF.close()
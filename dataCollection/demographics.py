DEM_F = open( "demographics.csv", "a+")

rightOrLeft = input("enter werher the participant is right or left handed ")

wristSize = input("enter the participants wrist size ")

sex = input("enter the participants sex")

height = input("enter the participants height")



print("writing: " + str(wristSize) + "," + str(rightOrLeft) + str(sex) + "," + str(height))

DEM_F.write(str(wristSize) + "," + str(rightOrLeft) + str(sex) + "," + str(height))
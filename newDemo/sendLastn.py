import requests
import os
import sys
import base64



sessions = os.listdir("data/")
#print(sessions)
sessionImgs = os.listdir("data/" + sessions[-1])
#print(sessionImgs)


url = sys.argv[1]

lastn = int(sys.argv[2])

lastFew = sessionImgs[-1*lastn:]
print(lastFew)

data = {"count" : str(lastn)}
c=0
for i in lastFew:
    image_path = "data/" + sessions[-1] + "/" + i
    b64_image = ""
    # Encoding the JPG,PNG,etc. image to base64 format
    with open(image_path, "rb") as imageFile:
        b64_image = base64.b64encode(imageFile.read())
        data[str(c)]=b64_image
        c = c + 1

#print(data)
# sending post request and saving response as response object
r = requests.post(url=url, data=data)



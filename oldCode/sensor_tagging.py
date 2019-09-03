## The follwoing code splits ALl the sensor data and re-arranges them into their corresponding file
## Note: This code should be executed only after the video splitting.

## Neccesary Imports
import os
from datetime import datetime
import csv
import pandas as pd

## This is the date format used observe that some are lower case and some are upper case they have different meanings, when updating chen datetime library
format_ = '%d-%m-%Y-%H-%M-%S'

## This is the path of trial folder, Change path name depending on experiment.
path = "~Documents/trial5/"
docs = os.listdir(path)

## The following 4 lines iterates through all the files and picks the sensor data files. And appends the file name to the tagPath to further process 
for doc in docs:
	if doc.startswith('trial5-') and doc.endswith('.csv'):
		tagsPath = "~/Documents/trial5/" + doc
		tagsP = "~/Documents/trial5/tags.csv"


		## The following is data preprocessing, at the end we re-arrange the data as lists of list. 
		## Each element in inside has 3 values
		## The number of elements in outside is the total number of readings
		with open(tagsPath) as file:
		    f = file.read()
		    vals = f.split('),')
		    vals = [item.strip('( ').split(', ') for item in vals]
		    outside = []
		    for r in vals:
		        if len(r) == 3:
		            inside = []
		            for c in r:
		                if c == None:
		                    inside.append(0.0)
		                else:
		                    inside.append(float(c))
		            outside.append(inside)

		## The following 4 lines of code is to extract utc time stamp from the filename
		## Then convert it the format specified in the top
		utcStamp = (tagsPath.split('.')[1])[:10]
		ts = int(utcStamp)
		dataStartTag = datetime.utcfromtimestamp(ts).strftime(format_)
		startObj = datetime.strptime(dataStartTag, format_)


		## The following lines parse the tags.csv file and extracts the experiment number, ID, start and end time stamps
		## in the format specified at the beginning
		tags = pd.read_csv(tagsP, header=None)
		length_to_use = len(tags.columns) - 1

		expIdx = list(range(0, length_to_use, 4))
		expNameIdx = list(range(1, length_to_use, 4))
		startIdx = list(range(2, length_to_use, 4))
		endIdx = list(range(3, length_to_use, 4))

		experimentId = list(tags.iloc[0, expIdx])
		experimentId = [x[1:] for x in experimentId]

		experimentTag = list(tags.iloc[0, expNameIdx])

		startTag = list(tags.iloc[0, startIdx])
		startTag = [(x.split('.')[1])[:10] for x in startTag]

		endTag = list(tags.iloc[0, endIdx])
		endTag = [x[:-1] for x in endTag]
		endTag = [(x.split('.')[1])[:10] for x in endTag]


		## The following lines convert start and end time stamps into start and end indices
		## ex: start, end before 2 mins 10 secs - 2 mins 16 secs is now changes to indices from 2600 - 2720 readings
		startTag = [int(x) for x in startTag]
		startTag = [datetime.utcfromtimestamp(ts).strftime(format_) for ts in startTag]
		startTagObj = [datetime.strptime(x, format_) for x in startTag]
		startSec = [((x - startObj).total_seconds(), 60) for x in startTagObj]
		startFrames = [int(x[0] * 20) for x in startSec]


		endTag = [int(x) for x in endTag]
		endTag = [datetime.utcfromtimestamp(ts).strftime(format_) for ts in endTag]
		endTagObj = [datetime.strptime(x, format_) for x in endTag]
		endSec = [((x - startObj).total_seconds(), 60) for x in endTagObj]
		endFrames = [int(x[0] * 20) for x in endSec]

		## The following code writes the sensor datat into a csv file in their corresponding folder
		for idx, (start, stop) in enumerate(zip(startFrames, endFrames)):
			name = "/home/local/ASUAD/bnagaban/Desktop/Tags_trial5/" + str(experimentId[idx]) + "/" + str(experimentTag[idx]) + "/" + (tagsPath.split('/')[-1]).split('-')[2] + ".csv"
			with open(name, "w") as f:
				writer =  csv.writer(f)
				content = outside[start:stop]
				writer.writerows(content)





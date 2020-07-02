import os
import sys
import pandas as pd
from flask import current_app as curr_app


def AddingtoCSV( filePath, tagData):
    csvPath = filePath + "/updated_csv"
    file_data = pd.read_csv( csvPath + "/final.csv")

    #Adding new column to add the tags in round-1
    file_data['tag_round1'] = "" # initialize a new column with all zero values
    #df.loc[df['timestamp'] == '1587950771.71122']
    #Saving the file after the tag column
    for value in tagData:
        tval = tagData[value]
        val = float(value.split(".jpg")[0])
        row = file_data.index[file_data['timestamp'] == val]
        print(val)
        print(row)
        if(len(row)>0):
            file_data.at[row[0],'tag_round1'] = tval 

    file_data.to_csv( csvPath + '/afterRound1.csv')
    # v4_data.to_csv( '/final.csv') 
    print("Final csv file after round-1 is generated successfully.")

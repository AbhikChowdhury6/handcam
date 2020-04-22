from zipfile import ZipFile

# This creates a ZipFile obj and load Archive.zip in it
with ZipFile('Archive.zip', 'r') as zipObj:
    # This extracts all the content of the zip file in the current directory.
    zipObj.extractall()
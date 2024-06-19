from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth 
from pathlib import Path
import numpy as np
import os
import cv2 as cv
path = Path().absolute()

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
"""
DOWNLOADS SHIT
"""
# Define the ID of the folder from which you want to download files
folder_id = '14-uekYXnSR2GOyVDEzPl866OFSf0IO2e'  # Replace with the actual folder ID

# List all files in the folder
file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

# Specify the local directory where you want to download files
local_directory = 'downloaded'  # Replace with your desired directory

# Create the local directory if it doesn't exist
if not os.path.exists(local_directory):
    os.makedirs(local_directory)

# Download each file from the folder
for file in file_list:
    file.GetContentFile(os.path.join(local_directory, file['title']))

print("Downloaded all files from the folder.")
"""
PROCESSES SHIT
"""
def processImage(p):
    image = cv.imread("downloaded/" + p)

    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    lower_yellow = (20, 0, 100)
    upper_yellow = (30, 15, 255)

    # Create a mask to isolate yellow regions in the image
    yellow_mask = cv.inRange(hsv_image, lower_yellow, upper_yellow)

    # Extract the yellow channel by bitwise ANDing the original image with the mask
    yellow_channel = cv.bitwise_and(image, image, mask=yellow_mask)

    print(os.path.join(path, 'processed', p))
    # Save or display the yellow channel image
    cv.imwrite(os.path.join(path, 'processed', p), yellow_channel)
    width, height, channels = image.shape
    return np.sum(yellow_mask > 0)/(width*height)

listOfDataShit = []
for filename in os.listdir("downloaded"):
    listOfDataShit.append(processImage(filename))
    print("Processed ", filename)
"""
UPLOADS SHIT
"""
parent_folder_id = '1oBZvDrszfXM02FEDuAKiFjbgYTG-9h6I'
# replace the value of this variable 
# with the absolute path of the directory 
path = os.path.join(path, "processed")   
   
# iterating thought all the files/folder 
# of the desired directory 
print(path)
csv = ','.join(os.listdir(path)) + "\n" + ','.join(np.char.mod('%f', listOfDataShit))
with open("processed/Output.csv", "w") as text_file:
    text_file.write(csv)

f = drive.CreateFile({'title': "Output.csv", 'parents': [{'id': parent_folder_id}]})
f.SetContentFile(os.path.join(path, "Output.csv"))


for x in os.listdir(path): 
    print(x)
    f = drive.CreateFile({'title': x, 'parents': [{'id': parent_folder_id}]})
    f.SetContentFile(os.path.join(path, x)) 
    f.Upload()

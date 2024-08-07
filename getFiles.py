from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth 
from pathlib import Path
import os
import cv2 as cv
path = Path().absolute()

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
"""
DOWNLOADS STUFF
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
PROCESSES STUFF
"""
def processImage(p):
    image = cv.imread("downloaded/" + p)

    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    lower_yellow = (5, 0, 0)
    upper_yellow = (50, 255, 255)

    # Create a mask to isolate yellow regions in the image
    yellow_mask = cv.inRange(hsv_image, lower_yellow, upper_yellow)

    # Extract the yellow channel by bitwise ANDing the original image with the mask
    yellow_channel = cv.bitwise_and(image, image, mask=yellow_mask)

    print(os.path.join(path, 'processed', p))
    # Save or display the yellow channel image
    cv.imwrite(os.path.join(path, 'processed', p), yellow_channel)

for filename in os.listdir("downloaded"):
    processImage(filename)
    print("Processed ", filename)
"""
UPLOADS STUFF
"""
parent_folder_id = '1oBZvDrszfXM02FEDuAKiFjbgYTG-9h6I'
# replace the value of this variable 
# with the absolute path of the directory 
path = os.path.join(path, "processed")   
   
# iterating thought all the files/folder 
# of the desired directory 
print(path)
for x in os.listdir(path): 
    print(x)
    f = drive.CreateFile({'title': x, 'parents': [parent_folder_id]})
    f.SetContentFile(os.path.join(path, x)) 
    f.Upload()
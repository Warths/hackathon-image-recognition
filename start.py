from imageprocessing import Imageprocessing
from os import scandir
import cv2
import requests

# source to analyze
img = cv2.imread("src/3.jpg")
# Central server
ip = "http://192.168.1.200:5000/data"
brightness_scale = Imageprocessing(img, img, 0, "Brightness_system")
brightness = brightness_scale.get_global_brightness()
available = 0
total_place = 0
# Masks corresponding to each parking space
# naming convention : $name-$threshold.png (or any compatible format)
# $name has a limit of 3 characters, enough for thousands of different names
# $threshold can be any number, needs to be calibrated, return different values if parking place is or isn't empty
for entry in scandir('masks/'):
    if not entry.name.startswith('.') and entry.is_dir() is not True:
        total_place += 1
        processing = Imageprocessing(img, cv2.imread('masks/' + entry.name), int((int(entry.name[4:-4]))), entry.name[0:3])
        if processing.is_available():
            available += 1

handi_available = 0
handi_total_place = 0
for entry in scandir('handi/'):
    if not entry.name.startswith('.') and entry.is_dir() is not True:
        handi_total_place += 1
        processing = Imageprocessing(img, cv2.imread('handi/' + entry.name), (int(entry.name[4:-4])), entry.name[0:3])
        if processing.is_available():
            handi_available += 1

all_available = available + handi_available
all_total_place = handi_total_place + total_place

print(str(all_available) + ' places dispo sur ' + str(all_total_place) + ' (dont '+ str(handi_available) + ' sur ' + str(handi_total_place) + ' places pour personnes à mobilité réduite)')

request_data = {
    "camera_id": "Parking_name_and_camera_ID_here",
    "total_place": total_place,
    "available_place": available,
    "handi_total_place": handi_total_place,
    "handi_available_place": handi_available
}
try:
    request = requests.post(ip, data=request_data)
    if request.status_code == 200 and request.json()['success']:
        print("Server updated")
    else:
        print("There's something wrong")
except:
    print("Server connection didn't succeed")

#!/usr/bin/env python3
import requests
from os import listdir

# This example shows how a file can be uploaded using
# The Python Requests module

url = "http://localhost/upload/"


def upload(file, url):
    with open(file, "rb") as opened:
        requests.post(url, files={"file": opened})


# set image dir:
img_dir = "supplier-data/images/"

# gather list of image files:
img_files = [img_dir + f for f in listdir(img_dir) if f.endswith(".jpeg")]
for file in img_files:
    upload(file, url)

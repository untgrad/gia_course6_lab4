#!/usr/bin/env python3
from os import listdir, path
from unicodedata import normalize
import requests
import json

# set text dir:
txt_dir = "supplier-data/descriptions/"

# gather list of text files:
text_files = [txt_dir + f for f in listdir(txt_dir) if f.endswith(".txt")]

# read text entry:
def getEntry(file):
    # get entry id & set image file name:
    entry_id = path.splitext(path.basename(file))[0]
    img_name = entry_id + ".jpeg"

    # read lines in file, assign to vars:
    with open(file) as f:
        lines = f.read().strip().splitlines()
    name, weight, description = lines

    # reformat weight to integer:
    weight = int(weight.replace(" lbs", ""))

    # set & return entry object:
    keys = ["name", "weight", "description", "image_name"]
    vals = [name, weight, description, img_name]
    entry = dict(zip(keys, vals))
    return entry


url = "http://localhost/fruits/"
for file in text_files:
    data = getEntry(file)
    response = requests.post(url, data=data)
    if response.ok:
        print("uploaded data")
    else:
        print(f"error: {response.status_code}")

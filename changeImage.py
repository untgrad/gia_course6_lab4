#!/usr/bin/env python3
from os import listdir, path
from PIL import Image

# set image dir:
img_dir = "supplier-data/images/"

# set reprocess vars:
rx_size = (600, 400)
rx_frmt = "JPEG"

# gather list of image files:
img_files = [f for f in listdir(img_dir) if f.endswith(".tiff")]

# reprocess images:
for file in img_files:
    src_img = Image.open(img_dir + file)
    new_img = src_img.resize(rx_size)
    # NOTE: we need to convert to RGB here to avoid error:
    new_img = new_img.convert("RGB")
    file, ext = path.splitext(file)
    file += ".jpeg"
    new_img.save(img_dir + file, rx_frmt)

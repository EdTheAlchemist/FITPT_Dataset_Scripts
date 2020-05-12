from __future__ import print_function, division

import sys
sys.path.insert(0, './Constants')

##### MAIN IMPORTS #####

from Paths import INSTAGRAM_POSTS_FOLDER_PATH, INSTAGRAM_PROF_PICS_FOLDER_PATH, TWITTER_PROF_PICS_FOLDER_PATH
from Paths import IMAGGA_INSTAGRAM_POST_FOLDER_PATH, IMAGGA_INSTAGRAM_PROF_FOLDER_PATH, IMAGGA_TWITTER_PROF_FOLDER_PATH
from Paths import FILTERED_USER_FILE_PATH
from APIs import API_KEY, API_SECRET, API_ENDPOINT

import pandas as pd
import requests
import os
import json

##### CONSTANTS #####

FOLDER_PAIRS = [
	[INSTAGRAM_POSTS_FOLDER_PATH, IMAGGA_INSTAGRAM_POST_FOLDER_PATH],
	[INSTAGRAM_PROF_PICS_FOLDER_PATH, IMAGGA_INSTAGRAM_PROF_FOLDER_PATH],
	[TWITTER_PROF_PICS_FOLDER_PATH, IMAGGA_TWITTER_PROF_FOLDER_PATH]
]
AUTH = (API_KEY, API_SECRET)

##### START OF SCRIPT #####

# Run through each folder with images to process
for FOLDER_PAIR in FOLDER_PAIRS:

	# Define input and output folders
	input_folder = FOLDER_PAIR[0]
	output_folder = FOLDER_PAIR[1]

	# Extract filenames of each image 
	images = [filename for filename in os.listdir(input_folder) if filename != ".DS_Store"]
	print("Total images in %s: %d" % (input_folder, len(images)))

	# Remove images from the query list that have tags already and get count of total images
	existing_images = [filename[7:-5] for filename in os.listdir(output_folder)]
	images = [filename for filename in images if filename[:-4] not in existing_images]
	images_count = len(images)
	print("Total images already tagged: %d" % (len(existing_images)))
	print("Remaining images to tag: %d" % (len(images)))

	# Start going through each image in the filtered list of images
	for i, image_file in enumerate(images):
		# Get full path to file
		image_path = os.path.join(input_folder, image_file)

		print('[%s / %s] %s processing ' % (i + 1, images_count, image_path))

		# HTTP request to imagga's tagging endpoint
		response = requests.post(
			'https://api.imagga.com/v2/tags',
			auth=AUTH,
			files={'image': open(image_path, 'rb')})

		# Save JSON response w/ filename same as input image but with "imagga_" appended at the front of the string
		file_name = image_file.split(".")[0]
		with open(output_folder + "imagga_%s.json" % file_name, 'w') as f:
			json.dump(response.json(), f, ensure_ascii=False, indent=4)

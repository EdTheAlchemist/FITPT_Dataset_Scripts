from __future__ import print_function, division

import sys
sys.path.insert(0, './Constants')

##### MAIN IMPORTS #####

from Paths import FILTERED_USER_FILE_PATH
from Paths import INSTA_POST_FILE_PATH, TWITTTER_POST_FILE_PATH
from Paths import INSTAGRAM_POSTS_FOLDER_PATH, INSTAGRAM_PROF_PICS_FOLDER_PATH, TWITTER_PROF_PICS_FOLDER_PATH
from math import sqrt

import pandas as pd
import numpy as np

import csv
import os

##### FUNCTIONS #####

##### START OF SCRIPT #####

# Load in filtered user data
user_df = pd.read_csv(FILTERED_USER_FILE_PATH)
user_df.set_index("UserID", inplace=True)

# Define user ID lists
twita_user_list = user_df[user_df.HasInstagram].index.tolist()
insta_user_list = user_df[user_df.HasTwitter].index.tolist()
both_user_list = user_df[(user_df.HasTwitter & user_df.HasInstagram)].index.tolist()

print("Twitter users: %d" % len(twita_user_list))
print("Instagram users: %d" % len(insta_user_list))
print("Both account users: %d" % len(both_user_list))
"""
# Load in text posts from CSV files
twita_text_df = pd.read_csv(INSTA_POST_FILE_PATH, encoding="utf-8", delimiter=',', quoting=csv.QUOTE_ALL)
twita_text_df.set_index("InstaPostID", inplace=True)
insta_text_df = pd.read_csv(TWITTTER_POST_FILE_PATH, encoding="utf-8", delimiter=',', quoting=csv.QUOTE_ALL)
insta_text_df.set_index("TweetID", inplace=True)

# Extract counts of text posts per user
twita_text_df = twita_text_df['UserID'].value_counts()
insta_text_df = insta_text_df['UserID'].value_counts()

# Generate dummy data such that new rows represent users w/ no posts
# This is done so stat extraction later had proper values
twita_text_df = twita_text_df.append(pd.Series({x:0 for x in set(twita_user_list) - set(twita_text_df.index.tolist())}))
insta_text_df = insta_text_df.append(pd.Series({x:0 for x in set(insta_user_list) - set(insta_text_df.index.tolist())}))
"""
# Load in filenames for all Instagram post images
insta_post_image_df = pd.DataFrame([{'UserID': filename.split('_')[2], 'PostID': filename.split('_')[1]} for filename in os.listdir(INSTAGRAM_POSTS_FOLDER_PATH) if filename != ".DS_Store"])
insta_post_image_df = insta_post_image_df['UserID'].value_counts()

# Generate dummy data such that new rows represent users w/ no posts
# This is done so stat extraction later had proper values
insta_post_image_df = insta_post_image_df.append(pd.Series({x:0 for x in set(insta_user_list) - set(insta_post_image_df.index.tolist())}))

# Load in filenames for profile pictures
insta_prof_image_df = pd.Series([filename.split('_')[2][:-4] for filename in os.listdir(INSTAGRAM_PROF_PICS_FOLDER_PATH) if filename != ".DS_Store"])
twita_prof_image_df = pd.Series([filename.split('_')[2][:-4] for filename in os.listdir(TWITTER_PROF_PICS_FOLDER_PATH) if filename != ".DS_Store"])

print(insta_post_image_df) # ig_128502_1820_.jpe
print(insta_prof_image_df) # ig_pp_427.jpe
print(twita_prof_image_df) # tw_pp_2686.jpe


exit()

# Add in dummy rows to simulate users w/ no posts


# 
groups = ["Twitter", "Instagram", "Both"]

for group in groups:
	group_name = group[0]
	list_of_users = group[1]
	statistics = {'group_name': group_name}

	if group_name == "Both":
		twita_text_df = twita_text_df[twita_text_df['UserID'].isin(both_user_list)]
		insta_df = insta_df[insta_df['UserID'].isin(both_user_list)]

	if group_name in ["Twitter", "Both"]:
		statistics['num_of_users'] = len(list_of_users)
		statistics['num_of_posts'] = len(twita_text_df)

	else:
		pass





### TEXT / CAPTION STATISTICS ###



# Instagram posts
post_counts = insta_text_df['UserID'].value_counts()
total_users = len(insta_user_lists)
print(len(post_counts))

post_counts = post_counts.append(pd.Series({x:0 for x in set(insta_user_lists) - set(post_counts.index.tolist())}))


print(len(post_counts))

exit()

print("Total Instagram posts: %d | Total Users: %d" % (insta_text_df['UserID'].value_counts().sum(), len(insta_text_df['UserID'].value_counts())))
print("Avg Instagram posts per user:", compute_mean(insta_text_df['UserID'].value_counts(), len(insta_user_lists)))
print("Std Instagram posts per user:", compute_std(insta_text_df['UserID'].value_counts(), len(insta_user_lists)))

print("Total Instagram posts w/o text:", len(insta_text_df[insta_text_df["Caption"] == np.NaN]))

print(compute_std(pd.Series([10,10,8,8,8,4]), 6))
print(pd.Series([10,10,8,8,8,4]).std())
# Twitter posts

### IMAGE STATISTICS ###

## PROFILE PICTURES ##

# Instagram posts

# Twitter Posts

## INSTAGRAM POST IMAGES ##

# Filtering for Instagram posts
#insta_post_filenames = [f for f in listdir(INSTAGRAM_POSTS_FOLDER_PATH) if isfile(join(INSTAGRAM_POSTS_FOLDER_PATH, f))]

# Filtering for Instagram profile pictures
#insta_prof_filenames = [f for f in listdir(INSTAGRAM_PROF_PICS_FOLDER_PATH) if isfile(join(INSTAGRAM_PROF_PICS_FOLDER_PATH, f))]

# Filtering for Twitter profile pictures
#twita_prof_filenames = [f for f in listdir(TWITTER_PROF_PICS_FOLDER_PATH) if isfile(join(TWITTER_PROF_PICS_FOLDER_PATH, f))]








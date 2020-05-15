from __future__ import print_function, division

import sys
sys.path.insert(0, './Constants')

##### MAIN IMPORTS #####

from Paths import FILTERED_USER_FILE_PATH, USER_POST_STATS_FILE_PATH
from Paths import INSTA_POST_FILE_PATH, TWITTTER_POST_FILE_PATH
from Paths import INSTAGRAM_POSTS_FOLDER_PATH, INSTAGRAM_PROF_PICS_FOLDER_PATH, TWITTER_PROF_PICS_FOLDER_PATH

import pandas as pd

import csv
import os

##### FUNCTIONS #####

# See note below for rational of function
def add_dummy_rows(s, user_list):
	return s.append(pd.Series({x:0 for x in set(user_list) - set(s.index.tolist())}))

##### START OF SCRIPT #####

# Load in filtered user data
user_df = pd.read_csv(FILTERED_USER_FILE_PATH)
user_df.set_index("UserID", inplace=True)

# Define user ID lists
insta_user_list = user_df[user_df.HasInstagram].index.tolist()
twita_user_list = user_df[user_df.HasTwitter].index.tolist()
both_user_list = user_df[(user_df.HasTwitter & user_df.HasInstagram)].index.tolist()

print("Twitter users: %d" % len(twita_user_list))
print("Instagram users: %d" % len(insta_user_list))
print("Both account users: %d" % len(both_user_list))

# Load in Instagram text posts from CSV file and fix dataframe
# Note: 2nd line is for processing of number of posts w/o caption
insta_text_df = pd.read_csv(INSTA_POST_FILE_PATH, encoding="utf-8", delimiter=',', quoting=csv.QUOTE_ALL)
insta_null_text_df = insta_text_df[insta_text_df['Caption'].isnull()]
insta_text_df = insta_text_df['UserID'].value_counts()
insta_null_text_df = insta_null_text_df['UserID'].value_counts()
insta_text_df.index = insta_text_df.index.map(int)
insta_null_text_df.index = insta_null_text_df.index.map(int)

# Load in Twitter text posts from CSV file and fix dataframe
twita_text_df = pd.read_csv(TWITTTER_POST_FILE_PATH, encoding="utf-8", delimiter=',', quoting=csv.QUOTE_ALL)
twita_text_df = twita_text_df['UserID'].value_counts()
twita_text_df.index = twita_text_df.index.map(int)

# Load in filenames for all Instagram post images and convert to dataframe
insta_post_image_df = pd.DataFrame([{'UserID': int(filename.split('_')[2]), 'PostID': filename.split('_')[1]} for filename in os.listdir(INSTAGRAM_POSTS_FOLDER_PATH) if filename != ".DS_Store"])
insta_post_image_df = insta_post_image_df['UserID'].value_counts()

# Load in filenames for profile pictures (both Instagram and Twitter) and convert to dataframe
insta_prof_image_df = pd.Series([filename.split('_')[2][:-4] for filename in os.listdir(INSTAGRAM_PROF_PICS_FOLDER_PATH) if filename != ".DS_Store"]).astype(int)
twita_prof_image_df = pd.Series([filename.split('_')[2][:-4] for filename in os.listdir(TWITTER_PROF_PICS_FOLDER_PATH) if filename != ".DS_Store"]).astype(int)

# Generate dummy data for missing rows; New rows represent users w/o posts
# I.e. since they had no posts, their UserID wasn't in their respective lists
# This is done so statistics extraction returns proper values
twita_text_df = add_dummy_rows(twita_text_df, twita_user_list)
insta_text_df = add_dummy_rows(insta_text_df, insta_user_list)
insta_post_image_df = add_dummy_rows(insta_post_image_df, insta_user_list)

# Start of extraction of statistics
group_names = ["Twitter", "Instagram", "Both"]
statistics_per_group = []
for group_name in group_names:
	# Condition modifying all dfs to retain users with both accounts
	if group_name == "Both":
		twita_text_df = twita_text_df[twita_text_df.index.isin(both_user_list)]
		insta_text_df = insta_text_df[insta_text_df.index.isin(both_user_list)]
		insta_post_image_df = insta_post_image_df[insta_post_image_df.index.isin(both_user_list)]
		insta_prof_image_df = insta_prof_image_df[insta_prof_image_df.isin(both_user_list)]
		twita_prof_image_df = twita_prof_image_df[twita_prof_image_df.isin(both_user_list)]
		insta_null_text_df = insta_null_text_df[insta_null_text_df.isin(both_user_list)]

	statistics_per_group.append({
		'group_name': group_name,
		
		# Twitter statistics
		'twitter_total_users': 0.0 if group_name == "Instagram" else len(twita_text_df),
		'twitter_total_posts': 0.0 if group_name == "Instagram" else twita_text_df.sum(),
		'twitter_avg_posts': 0.0 if group_name == "Instagram" else twita_text_df.mean(),
		'twitter_std_posts': 0.0 if group_name == "Instagram" else twita_text_df.std(),
		'twitter_min_posts': 0.0 if group_name == "Instagram" else twita_text_df.min(),
		'twitter_max_posts': 0.0 if group_name == "Instagram" else twita_text_df.max(),
		'twitter_total_prof_pics': 0.0 if group_name == "Instagram" else len(twita_prof_image_df),

		# Instagram statistics
		'instagram_total_users': 0.0 if group_name == "Twitter" else len(insta_text_df),
		'instagram_total_posts': 0.0 if group_name == "Twitter" else insta_text_df.sum(),
		'instagram_avg_posts': 0.0 if group_name == "Twitter" else insta_text_df.mean(),
		'instagram_std_posts': 0.0 if group_name == "Twitter" else insta_text_df.std(),
		'instagram_min_posts': 0.0 if group_name == "Twitter" else insta_text_df.min(),
		'instagram_max_posts': 0.0 if group_name == "Twitter" else insta_text_df.max(),
		'instagram_total_posts_wo_text': 0.0 if group_name == "Twitter" else insta_null_text_df.sum(),
		'instagram_total_prof_pics': 0.0 if group_name == "Twitter" else len(insta_prof_image_df),
		'instagram_total_images': 0.0 if group_name == "Twitter" else insta_post_image_df.sum(),
		'instagram_avg_images': 0.0 if group_name == "Twitter" else insta_post_image_df.mean(),
		'instagram_std_images': 0.0 if group_name == "Twitter" else insta_post_image_df.std(),
		'instagram_min_images': 0.0 if group_name == "Twitter" else insta_post_image_df.min(),
		'instagram_max_images': 0.0 if group_name == "Twitter" else insta_post_image_df.max()
	})

# Convert list of statistics to dataframe and save to csv
df = pd.DataFrame(statistics_per_group)
df.set_index("group_name", inplace=True)
df.to_csv(USER_POST_STATS_FILE_PATH)


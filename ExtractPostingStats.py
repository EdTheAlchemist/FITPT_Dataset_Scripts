from __future__ import print_function, division

import sys
sys.path.insert(0, './Constants')

##### MAIN IMPORTS #####

from Paths import FILTERED_USER_FILE_PATH
from Paths import INSTA_POST_FILE_PATH, TWITTTER_POST_FILE_PATH
from Paths import INSTAGRAM_POSTS_FOLDER_PATH, INSTAGRAM_PROF_PICS_FOLDER_PATH, TWITTER_PROF_PICS_FOLDER_PATH

import pandas as pd
import numpy as np

##### START OF SCRIPT #####

# Load in filtered user data
user_df = pd.read_csv(FILTERED_USER_FILE_PATH)
user_df.set_index("UserID", inplace=True)

# Get user names from filtered list of users
twita_user_lists = user_df[user_df.HasTwitter].index.tolist()
insta_user_lists = user_df[user_df.HasInstagram].index.tolist()
both_user_lists = user_df[(user_df.HasTwitter & user_df.HasInstagram)].index.tolist()

### TEXT / CAPTION STATISTICS ###

# Load in CSV files
#twita_text_df = pd.read_csv(TWITTTER_POST_FILE_PATH, encoding="utf-8")
#twita_text_df.set_index("TweetID", inplace=True)
insta_text_df = pd.read_csv(INSTA_POST_FILE_PATH, encoding="utf-8", delimiter=',')
insta_text_df.set_index("InstaPostID", inplace=True)

# Instagram posts
print("Total Instagram posts:", insta_text_df['UserID'].value_counts().sum())
print("Avg Instagram posts per user:", insta_text_df['UserID'].value_counts().mean())
print("Std Instagram posts per user:", insta_text_df['UserID'].value_counts().std())

print("Total Instagram posts w/o text", insta_text_df['UserID'][insta_text_df["Caption"] == np.nan])
print(insta_text_df[insta_text_df.UserID == 2])

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








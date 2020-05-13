from __future__ import print_function, division

import sys
sys.path.insert(0, './Constants')

##### MAIN IMPORTS #####

from Paths import FILTERED_USER_FILE_PATH
from Paths import INSTA_POST_FILE_PATH, TWITTTER_POST_FILE_PATH
from ftfy import fix_encoding

import pandas as pd
import csv

##### START OF SCRIPT #####

# Load in filtered user data
user_df = pd.read_csv(FILTERED_USER_FILE_PATH)
user_df.set_index("UserID", inplace=True)

# Get user names from filtered list of users
twita_user_lists = user_df[user_df.HasTwitter].index.tolist()
insta_user_lists = user_df[user_df.HasInstagram].index.tolist()

# Load in CSV files
twita_text_df = pd.read_csv(TWITTTER_POST_FILE_PATH, encoding="utf-8", sep=',')
twita_text_df.set_index("TweetID", inplace=True)
twita_text_df['Text'].fillna("", inplace=True)
insta_text_df = pd.read_csv(INSTA_POST_FILE_PATH, encoding="utf-8", sep=',')
insta_text_df.set_index("InstaPostID", inplace=True)
insta_text_df['Caption'].fillna("", inplace=True)

# For Instagram posts, remove URL column since that won't be needed moving forward
insta_text_df = insta_text_df[[u'UserID',u'DatePosted', u'Caption', u'LikesCount', u'Location']]

# Remove posts that belong to users that didn't qualify for participation
twita_text_df = twita_text_df[twita_text_df['UserID'].isin(twita_user_lists)]
insta_text_df = insta_text_df[insta_text_df['UserID'].isin(insta_user_lists)]

# Fix text encoding (must be in UTF-8)
twita_text_df['Text'] = twita_text_df['Text'].astype(unicode).apply(fix_encoding)
insta_text_df['Caption'] = insta_text_df['Caption'].astype(unicode).apply(fix_encoding)

# Save fixed files to input folders (there is no need to keep data that's from non-qualifying participants)
# Force all values to be quoted because of possible issues with line breaks
twita_text_df.to_csv(TWITTTER_POST_FILE_PATH, encoding="utf-8", sep=',', quoting=csv.QUOTE_ALL)
insta_text_df.to_csv(INSTA_POST_FILE_PATH, encoding="utf-8", sep=',', quoting=csv.QUOTE_ALL)

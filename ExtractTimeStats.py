from __future__ import print_function, division

import sys
sys.path.insert(0, './Constants')

##### MAIN IMPORTS #####

from Paths import USER_FILE_PATH, TWITTTER_POST_FILE_PATH, INSTA_POST_FILE_PATH, TIME_POSTS_PER_YEAR_FILE_PATH

import pandas as pd

##### FUNCTIONS #####

def extract_year_twitter(text):
	# Based on following format: '%a %b %d %H:%M:%S %z %Y'
	return text[-4:]

def extract_year_instagram(text):
	# Based on following format: '%Y-%m-%d %H:%M:%S'
	return text[:4]

##### START OF SCRIPT #####

# List to store posts per year of each platform
years = []

# Load in qualified users and extract the UserID (to remove posts from users who were removed)
users_df = pd.read_csv(USER_FILE_PATH)
users_list = users_df.UserID.tolist()
# Load in tweets and filter out tweets from users removed
tweets_df = pd.read_csv(TWITTTER_POST_FILE_PATH)
tweets_df.set_index("TweetID", inplace=True)
tweets_df = tweets_df[tweets_df['UserID'].isin(users_df.index)]
# Extract year from data_created based on string format (described in function above)
tweets_df['Date_Created'] = tweets_df['Date_Created'].apply(extract_year_twitter)
# Count dates and extract to a dictionary 
twitter_years_dict = tweets_df['Date_Created'].value_counts().to_dict()
# Label appropriately
twitter_years_dict['platform'] = "twitter"
# Add dictionary to list of years
years.append(twitter_years_dict)

##### Instagram follows similar process above, but with different function (because of different date format)
instagram_df = pd.read_csv(INSTA_POST_FILE_PATH)
instagram_df.set_index("InstaPostID", inplace=True)
instagram_df = instagram_df[instagram_df['UserID'].isin(users_df.index)]
instagram_df['DatePosted'] = instagram_df['DatePosted'].apply(extract_year_instagram)
instagram_years_dict = instagram_df['DatePosted'].value_counts().to_dict()
instagram_years_dict['platform'] = "instagram"
years.append(instagram_years_dict)

# Convert list of posts per year to dataframe and save to CSV file
time_df = pd.DataFrame(years)
time_df.set_index("platform", inplace=True)
time_df.to_csv(TIME_POSTS_PER_YEAR_FILE_PATH)

from __future__ import print_function, division

import sys
sys.path.insert(0, './Constants')

##### MAIN IMPORTS #####

from Paths import FILTERED_USER_FILE_PATH, INSTA_PROFILE_FILE_PATH, TWITTER_PROFILE_FILE_PATH, ACCOUNT_RELATED_DATA_FILE_PATH

import pandas as pd

# Load in filtered user data
user_df = pd.read_csv(FILTERED_USER_FILE_PATH)
user_df.set_index("UserID", inplace=True)

# Get all filtered users
insta_user_list = user_df[user_df.HasInstagram].index.tolist()
twita_user_list = user_df[user_df.HasTwitter].index.tolist()
both_user_list = user_df[(user_df.HasTwitter & user_df.HasInstagram)].index.tolist()

# List to hold all statistics
statistics = []

# Load in Social Media Data
twitter_df = pd.read_csv(TWITTER_PROFILE_FILE_PATH)
twitter_df = twitter_df[twitter_df['UserID'].isin(twita_user_list)]
instagram_df = pd.read_csv(INSTA_PROFILE_FILE_PATH)
instagram_df = instagram_df[instagram_df['UserID'].isin(insta_user_list)]

statistics.append({
	'Platform': 'Twitter-all',
	'AvgFollowingCount': twitter_df['FollowingCount'].mean(),
	'StdFollowingCount': twitter_df['FollowingCount'].std(),
	'AvgFollowersCount': twitter_df['FollowersCount'].mean(),
	'StdFollowersCount': twitter_df['FollowersCount'].std(),
	'AvgFavouritesCount': twitter_df['FavouritesCount'].mean(),
	'StdFavouritesCount': twitter_df['FavouritesCount'].std(),
	'AvgTweetCount': twitter_df['TweetCount'].mean(),
	'StdTweetCount': twitter_df['TweetCount'].std(),
	})

statistics.append({
	'Platform': 'Instagram-all',
	'AvgFollowingCount': instagram_df['FollowingCount'].mean(),
	'StdFollowingCount': instagram_df['FollowingCount'].std(),
	'AvgPostCount': instagram_df['PostCount'].mean(),
	'StdPostCount': instagram_df['PostCount'].std(),
	})

# Swap oveer to users w/ both accounts
twitter_df = twitter_df[twitter_df['UserID'].isin(both_user_list)]
instagram_df = instagram_df[instagram_df['UserID'].isin(both_user_list)]

statistics.append({
	'Platform': 'Twitter-both',
	'AvgFollowingCount': twitter_df['FollowingCount'].mean(),
	'StdFollowingCount': twitter_df['FollowingCount'].std(),
	'AvgFollowersCount': twitter_df['FollowersCount'].mean(),
	'StdFollowersCount': twitter_df['FollowersCount'].std(),
	'AvgFavouritesCount': twitter_df['FavouritesCount'].mean(),
	'StdFavouritesCount': twitter_df['FavouritesCount'].std(),
	'AvgTweetCount': twitter_df['TweetCount'].mean(),
	'StdTweetCount': twitter_df['TweetCount'].std(),
	})

statistics.append({
	'Platform': 'Instagram-both',
	'AvgFollowingCount': instagram_df['FollowingCount'].mean(),
	'StdFollowingCount': instagram_df['FollowingCount'].std(),
	'AvgPostCount': instagram_df['PostCount'].mean(),
	'StdPostCount': instagram_df['PostCount'].std(),
	})

statistics_df = pd.DataFrame(statistics)
statistics_df.set_index("Platform", inplace=True)
statistics_df.to_csv(ACCOUNT_RELATED_DATA_FILE_PATH)
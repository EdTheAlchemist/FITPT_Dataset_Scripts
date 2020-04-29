from __future__ import print_function, division

import sys
sys.path.insert(0, './Constants')

##### MAIN IMPORTS #####

from Paths import USER_FILE_PATH, PERSONALITY_FILE_PATH, INSTA_PROFILE_FILE_PATH, TWITTER_PROFILE_FILE_PATH, INSTA_POST_FILE_PATH, TWITTTER_POST_FILE_PATH, FILTERED_USER_FILE_PATH
from CollectionDates import COLLECTION_DATES

from datetime import datetime

import pandas as pd

##### CONSTANTS #####
TRAITS = [
	'Openness',
	'Conscientiousness',
	'Extraversion',
	'Agreeableness',
	'Neuroticism'
]

##### FUNCTIONS #####

week = 0
count = 0
def calculate_age(text):
	global week, count

	born = datetime.strptime(text, "%Y-%m-%d").date()
	day_of_collection = datetime.strptime(COLLECTION_DATES[week][0], "%d/%m/%Y").date()
	age = day_of_collection.year - born.year - ((day_of_collection.month, day_of_collection.day) < (born.month, born.day))

	count = count + 1
	if count > COLLECTION_DATES[week][1]:
		week = week + 1
	
	return age

##### START OF SCRIPT #####

# Load in CSV for all users (raw data)
user_df = pd.read_csv(USER_FILE_PATH, encoding='utf-8')
user_df.set_index("UserID", inplace=True)
user_df['Age'] = user_df['Birthdate'].apply(calculate_age)
user_df = user_df[['Sex', 'Nationality', 'Age']]

# Load in CSV of personality scores (raw data)
personality_df = pd.read_csv(PERSONALITY_FILE_PATH, encoding='utf-8')
personality_df.set_index("UserID", inplace=True)

# Identify users to removee (filters)
# (1) Age less than 18, (2) Nationality doesn't contain "Filipino", (3) Errors with personality scores
users_to_remove = []
users_to_remove += user_df.Age[user_df.Age < 18].index.tolist()
users_to_remove += user_df.Nationality[~user_df.Nationality.str.contains("Filipino")].index.tolist()
users_to_remove += personality_df.Answers[personality_df.Answers.str.contains("undefined")].index.tolist()
user_df = user_df[~user_df.index.isin(users_to_remove)]

# Load in Twitter account data
twitter_df = pd.read_csv(TWITTER_PROFILE_FILE_PATH, encoding='utf-8')
twitter_df.set_index("UserID", inplace=True)

# Load in Instagram account data
instagram_df = pd.read_csv(INSTA_PROFILE_FILE_PATH, encoding='utf-8')
instagram_df.set_index("UserID", inplace=True)

# Plot whether a participant has a Twitter and/or Instagram account
user_df["HasTwitter"] = user_df.index.isin(twitter_df.index)
user_df["HasInstagram"] = user_df.index.isin(instagram_df.index)
for trait in TRAITS:
	user_df[trait] = personality_df[trait]

# Save final file to CSV
user_df.to_csv(FILTERED_USER_FILE_PATH, encoding='utf-8')
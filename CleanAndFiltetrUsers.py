from __future__ import print_function, division

import sys
sys.path.insert(0, './Constants')

##### MAIN IMPORTS #####

from Paths import USER_FILE_PATH, PERSONALITY_FILE_PATH, INSTA_PROFILE_FILE_PATH, TWITTER_PROFILE_FILE_PATH, INSTA_POST_FILE_PATH, TWITTTER_POST_FILE_PATH, GENERATED_DATA_FOLDER_PATH
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

users_to_remove = []

user_df = pd.read_csv(USER_FILE_PATH, encoding='utf-8')
user_df.set_index("UserID", inplace=True)
user_df['Age'] = user_df['Birthdate'].apply(calculate_age)
user_df = user_df[['Sex', 'Nationality', 'Age']]

personality_df = pd.read_csv(PERSONALITY_FILE_PATH, encoding='utf-8')
personality_df.set_index("UserID", inplace=True)

users_to_remove += user_df.Age[user_df.Age < 18].index.tolist()
users_to_remove += user_df.Nationality[~user_df.Nationality.str.contains("Filipino")].index.tolist()
users_to_remove += personality_df.Answers[personality_df.Answers.str.contains("undefined")].index.tolist()
user_df = user_df[~user_df.index.isin(users_to_remove)]

twitter_df = pd.read_csv(TWITTER_PROFILE_FILE_PATH, encoding='utf-8')
twitter_df.set_index("UserID", inplace=True)

instagram_df = pd.read_csv(INSTA_PROFILE_FILE_PATH, encoding='utf-8')
instagram_df.set_index("UserID", inplace=True)

user_df["HasTwitter"] = user_df.index.isin(twitter_df.index)
user_df["HasInstagram"] = user_df.index.isin(instagram_df.index)
for trait in TRAITS:
	user_df[trait] = personality_df[trait]
	
user_df.to_csv(GENERATED_DATA_FOLDER_PATH + "filtered_users.csv", encoding='utf-8')
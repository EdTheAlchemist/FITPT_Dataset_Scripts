from __future__ import print_function, division

import sys
sys.path.insert(0, './Constants')

##### MAIN IMPORTS #####

from Paths import FILTERED_USER_FILE_PATH, USER_DEMOGRAPHICS_FILE_PATH

import pandas as pd

##### START OF SCRIPT #####

# Main dictionary to hold all demographics
demographics = []

# Load in filtered user data
filtered_user_df = pd.read_csv(FILTERED_USER_FILE_PATH, encoding='utf-8')
filtered_user_df.set_index("UserID", inplace=True)

# Create separate dfs for w/ twitter, w/ instagram and w/ both
# Each of these (+ total) forms 4 major group divisions
twitter_users_df = filtered_user_df[filtered_user_df['HasTwitter'] == True]
instagram_users_df = filtered_user_df[filtered_user_df['HasInstagram'] == True]
both_users_df = filtered_user_df[(filtered_user_df['HasTwitter'] == True) & (filtered_user_df['HasInstagram'] == True)]

# Demographics across all participants
demographics.append({
	'group': 'all',
	# Total participant count
	'pax_count': len(filtered_user_df),
	# Counts for each sex category
	'male': len(filtered_user_df[filtered_user_df['Sex'] == "Male"]),
	'female': len(filtered_user_df[filtered_user_df['Sex'] == "Female"]),
	'others': len(filtered_user_df[(filtered_user_df['Sex'] == "Decline to disclose") | (filtered_user_df['Sex'] == "Intersex")]),
	# Stats for age + counts per age group
	'age_mean': filtered_user_df['Age'].mean(),
	'age_std': filtered_user_df['Age'].std(),
	'age_18_20': len(filtered_user_df[(filtered_user_df['Age'] >= 18) & (filtered_user_df['Age'] <= 20)]),
	'age_21_23': len(filtered_user_df[(filtered_user_df['Age'] >= 21) & (filtered_user_df['Age'] <= 23)]),
	'age_24_26': len(filtered_user_df[(filtered_user_df['Age'] >= 24) & (filtered_user_df['Age'] <= 26)]),
	'age_gt_27': len(filtered_user_df[filtered_user_df['Age'] >= 27]),
	# Counts for Filipino and mixed-Filipino
	'filipino': len(filtered_user_df[filtered_user_df['Nationality'] == 'Filipino']),
	'both': len(filtered_user_df[filtered_user_df['Nationality'] != 'Filipino']),
	})

# Demographics for participants w/ Twitter accounts (same as above, but with different df)
demographics.append({
	'group': 'twitter',
	'pax_count': len(twitter_users_df),
	'male': len(twitter_users_df[twitter_users_df['Sex'] == "Male"]),
	'female': len(twitter_users_df[twitter_users_df['Sex'] == "Female"]),
	'others': len(twitter_users_df[(twitter_users_df['Sex'] == "Decline to disclose") | (twitter_users_df['Sex'] == "Intersex")]),
	'age_mean': twitter_users_df['Age'].mean(),
	'age_std': twitter_users_df['Age'].std(),
	'age_18_20': len(twitter_users_df[(twitter_users_df['Age'] >= 18) & (twitter_users_df['Age'] <= 20)]),
	'age_21_23': len(twitter_users_df[(twitter_users_df['Age'] >= 21) & (twitter_users_df['Age'] <= 23)]),
	'age_24_26': len(twitter_users_df[(twitter_users_df['Age'] >= 24) & (twitter_users_df['Age'] <= 26)]),
	'age_gt_27': len(twitter_users_df[twitter_users_df['Age'] >= 27]),
	'filipino': len(twitter_users_df[twitter_users_df['Nationality'] == 'Filipino']),
	'both': len(twitter_users_df[twitter_users_df['Nationality'] != 'Filipino']),
	})

# Demographics for participants w/ Instagram accounts (same as above, but with different df)
demographics.append({
	'group': 'instagram',
	'pax_count': len(instagram_users_df),
	'male': len(instagram_users_df[instagram_users_df['Sex'] == "Male"]),
	'female': len(instagram_users_df[instagram_users_df['Sex'] == "Female"]),
	'others': len(instagram_users_df[(instagram_users_df['Sex'] == "Decline to disclose") | (instagram_users_df['Sex'] == "Intersex")]),
	'age_mean': instagram_users_df['Age'].mean(),
	'age_std': instagram_users_df['Age'].std(),
	'age_18_20': len(instagram_users_df[(instagram_users_df['Age'] >= 18) & (instagram_users_df['Age'] <= 20)]),
	'age_21_23': len(instagram_users_df[(instagram_users_df['Age'] >= 21) & (instagram_users_df['Age'] <= 23)]),
	'age_24_26': len(instagram_users_df[(instagram_users_df['Age'] >= 24) & (instagram_users_df['Age'] <= 26)]),
	'age_gt_27': len(instagram_users_df[instagram_users_df['Age'] >= 27]),
	'filipino': len(instagram_users_df[instagram_users_df['Nationality'] == 'Filipino']),
	'both': len(instagram_users_df[instagram_users_df['Nationality'] != 'Filipino']),
	})

# Demographics for participants w/ bot Twitter and Instagram accounts (same as above, but with different df)
demographics.append({
	'group': 'both',
	'pax_count': len(both_users_df),
	'male': len(both_users_df[both_users_df['Sex'] == "Male"]),
	'female': len(both_users_df[both_users_df['Sex'] == "Female"]),
	'others': len(both_users_df[(both_users_df['Sex'] == "Decline to disclose") | (both_users_df['Sex'] == "Intersex")]),
	'age_mean': both_users_df['Age'].mean(),
	'age_std': both_users_df['Age'].std(),
	'age_18_20': len(both_users_df[(both_users_df['Age'] >= 18) & (both_users_df['Age'] <= 20)]),
	'age_21_23': len(both_users_df[(both_users_df['Age'] >= 21) & (both_users_df['Age'] <= 23)]),
	'age_24_26': len(both_users_df[(both_users_df['Age'] >= 24) & (both_users_df['Age'] <= 26)]),
	'age_gt_27': len(both_users_df[both_users_df['Age'] >= 27]),
	'filipino': len(both_users_df[both_users_df['Nationality'] == 'Filipino']),
	'both': len(both_users_df[both_users_df['Nationality'] != 'Filipino']),
	})

# Convert demographics list to dataframe and save to CSV
df = pd.DataFrame(demographics)
df.set_index("group", inplace=True)
df.to_csv(USER_DEMOGRAPHICS_FILE_PATH)

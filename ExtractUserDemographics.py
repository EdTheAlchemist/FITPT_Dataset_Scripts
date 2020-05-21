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
	# Percentage for each sex category
	'male': len(filtered_user_df[filtered_user_df['Sex'] == "Male"]) / len(filtered_user_df),
	'female': len(filtered_user_df[filtered_user_df['Sex'] == "Female"]) / len(filtered_user_df),
	'intersex': len(filtered_user_df[filtered_user_df['Sex'] == "Intersex"]) / len(filtered_user_df),
	'decline_to_disclose': len(filtered_user_df[filtered_user_df['Sex'] == "Decline to disclose"]) / len(filtered_user_df),
	# Stats for age + percentages per age group
	'age_mean': filtered_user_df['Age'].mean(),
	'age_std': filtered_user_df['Age'].std(),
	'age_18_20': len(filtered_user_df[(filtered_user_df['Age'] >= 18) & (filtered_user_df['Age'] <= 20)]) / len(filtered_user_df),
	'age_21_23': len(filtered_user_df[(filtered_user_df['Age'] >= 21) & (filtered_user_df['Age'] <= 23)]) / len(filtered_user_df),
	'age_24_26': len(filtered_user_df[(filtered_user_df['Age'] >= 24) & (filtered_user_df['Age'] <= 26)]) / len(filtered_user_df),
	'age_gt_27': len(filtered_user_df[filtered_user_df['Age'] >= 27]) / len(filtered_user_df),
	# Percentage for Filipino and mixed-Filipino
	'filipino': len(filtered_user_df[filtered_user_df['Nationality'] == 'Filipino']) / len(filtered_user_df),
	'both': len(filtered_user_df[filtered_user_df['Nationality'] != 'Filipino']) / len(filtered_user_df),
	})

# Demographics for participants w/ Twitter accounts (same as above, but with different df)
demographics.append({
	'group': 'twitter',
	'pax_count': len(twitter_users_df),
	'male': len(twitter_users_df[twitter_users_df['Sex'] == "Male"]) / len(twitter_users_df),
	'female': len(twitter_users_df[twitter_users_df['Sex'] == "Female"]) / len(twitter_users_df),
	'intersex': len(twitter_users_df[twitter_users_df['Sex'] == "Intersex"]) / len(twitter_users_df),
	'decline_to_disclose': len(twitter_users_df[twitter_users_df['Sex'] == "Decline to disclose"]) / len(twitter_users_df),
	'age_mean': twitter_users_df['Age'].mean(),
	'age_std': twitter_users_df['Age'].std(),
	'age_18_20': len(twitter_users_df[(twitter_users_df['Age'] >= 18) & (twitter_users_df['Age'] <= 20)]) / len(twitter_users_df),
	'age_21_23': len(twitter_users_df[(twitter_users_df['Age'] >= 21) & (twitter_users_df['Age'] <= 23)]) / len(twitter_users_df),
	'age_24_26': len(twitter_users_df[(twitter_users_df['Age'] >= 24) & (twitter_users_df['Age'] <= 26)]) / len(twitter_users_df),
	'age_gt_27': len(twitter_users_df[twitter_users_df['Age'] >= 27]) / len(twitter_users_df),
	'filipino': len(twitter_users_df[twitter_users_df['Nationality'] == 'Filipino']) / len(twitter_users_df),
	'both': len(twitter_users_df[twitter_users_df['Nationality'] != 'Filipino']) / len(twitter_users_df),
	})

# Demographics for participants w/ Instagram accounts (same as above, but with different df)
demographics.append({
	'group': 'instagram',
	'pax_count': len(instagram_users_df),
	'male': len(instagram_users_df[instagram_users_df['Sex'] == "Male"]) / len(instagram_users_df),
	'female': len(instagram_users_df[instagram_users_df['Sex'] == "Female"]) / len(instagram_users_df),
	'intersex': len(instagram_users_df[instagram_users_df['Sex'] == "Intersex"]) / len(instagram_users_df),
	'decline_to_disclose': len(instagram_users_df[instagram_users_df['Sex'] == "Decline to disclose"]) / len(instagram_users_df),
	'age_mean': instagram_users_df['Age'].mean(),
	'age_std': instagram_users_df['Age'].std(),
	'age_18_20': len(instagram_users_df[(instagram_users_df['Age'] >= 18) & (instagram_users_df['Age'] <= 20)]) / len(instagram_users_df),
	'age_21_23': len(instagram_users_df[(instagram_users_df['Age'] >= 21) & (instagram_users_df['Age'] <= 23)]) / len(instagram_users_df),
	'age_24_26': len(instagram_users_df[(instagram_users_df['Age'] >= 24) & (instagram_users_df['Age'] <= 26)]) / len(instagram_users_df),
	'age_gt_27': len(instagram_users_df[instagram_users_df['Age'] >= 27]) / len(instagram_users_df),
	'filipino': len(instagram_users_df[instagram_users_df['Nationality'] == 'Filipino']) / len(instagram_users_df),
	'both': len(instagram_users_df[instagram_users_df['Nationality'] != 'Filipino']) / len(instagram_users_df),
	})

# Demographics for participants w/ bot Twitter and Instagram accounts (same as above, but with different df)
demographics.append({
	'group': 'both',
	'pax_count': len(both_users_df),
	'male': len(both_users_df[both_users_df['Sex'] == "Male"]) / len(both_users_df),
	'female': len(both_users_df[both_users_df['Sex'] == "Female"]) / len(both_users_df),
	'intersex': len(both_users_df[both_users_df['Sex'] == "Intersex"]) / len(both_users_df),
	'decline_to_disclose': len(both_users_df[both_users_df['Sex'] == "Decline to disclose"]) / len(both_users_df),
	'age_mean': both_users_df['Age'].mean(),
	'age_std': both_users_df['Age'].std(),
	'age_18_20': len(both_users_df[(both_users_df['Age'] >= 18) & (both_users_df['Age'] <= 20)]) / len(both_users_df),
	'age_21_23': len(both_users_df[(both_users_df['Age'] >= 21) & (both_users_df['Age'] <= 23)]) / len(both_users_df),
	'age_24_26': len(both_users_df[(both_users_df['Age'] >= 24) & (both_users_df['Age'] <= 26)]) / len(both_users_df),
	'age_gt_27': len(both_users_df[both_users_df['Age'] >= 27]) / len(both_users_df),
	'filipino': len(both_users_df[both_users_df['Nationality'] == 'Filipino']) / len(both_users_df),
	'both': len(both_users_df[both_users_df['Nationality'] != 'Filipino']) / len(both_users_df),
	})

# Convert demographics list to dataframe and save to CSV
df = pd.DataFrame(demographics)
df.set_index("group", inplace=True)
df.to_csv(USER_DEMOGRAPHICS_FILE_PATH)

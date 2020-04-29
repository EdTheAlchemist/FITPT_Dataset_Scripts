from __future__ import print_function, division

import sys
sys.path.insert(0, './Constants')

##### MAIN IMPORTS #####

from Paths import PERSONALITY_FILE_PATH, FILTERED_USER_FILE_PATH, PERSONALITY_COOR_FILE_PATH, PERSONALITY_ITEM_SCORES_FILE_PATH, PERSONALITY_CRONBACHS_ALPHA_FILE_PATH, PERSONALITY_STATS_FILE_PATH, PERSONALITY_BINS_FILE_PATH

import pandas as pd

##### CONSTANTS #####

REVERSE_SCORING = {
	'1': 5,
	'2': 4,
	'3': 3,
	'4': 2,
	'5': 1
}
SCORES_TO_REVERSE = [6, 21, 31, 2, 12, 27, 37, 8, 18, 23, 43, 9, 24, 34, 35, 41]
ITEM_TO_TRAIT = {
	'Extraversion': [1, 6, 11, 16, 21, 26, 31, 36],
	'Agreeableness': [2, 7, 12, 17, 22, 27, 32, 37, 42],
	'Conscientiousness': [3, 8, 13, 18, 23, 28, 33, 38, 43],
	'Neuroticism': [4, 9, 14, 19, 24, 29, 34, 39],
	'Openness': [5, 10, 15, 20, 25, 30, 35, 40, 41, 44],
}
BINS = [x * .25 for x in range(4,21)]
##### FUNCTIONS #####

def reverse_score(number):
	return REVERSE_SCORING[str(number)]

# Taken from https://github.com/anthropedia/tci-stats/blob/master/tcistats/__init__.py
# Modified -- input is already of dataframe type
def cronbach_alpha(items):
    items_count = items.shape[1]
    variance_sum = float(items.var(axis=0, ddof=1).sum())
    total_var = float(items.sum(axis=1).var(ddof=1))
    
    return (items_count / float(items_count - 1) * (1 - variance_sum / total_var))

##### START OF SCRIPT #####

# Load in personality data
personality_df = pd.read_csv(PERSONALITY_FILE_PATH, encoding="utf-8")
personality_df.set_index("UserID", inplace=True)

# Load in filtered user data
filtered_user_df = pd.read_csv(FILTERED_USER_FILE_PATH, encoding='utf-8')
filtered_user_df.set_index("UserID", inplace=True)

# Remove / filter out participants who don't qualify / Retain those who do
personality_df = personality_df[personality_df.index.isin(filtered_user_df.index)]

# Get mean, std, min, and max for each trait and save to CSV file
stats = []
for trait in ITEM_TO_TRAIT:
	trait_df = personality_df[trait]
	temp_stats = {
		'trait': trait,
		'mean': trait_df.mean(),
		'std': trait_df.std(),
		'min': trait_df.min(),
		'max': trait_df.max()
	}
	stats.append(temp_stats)
stats_df = pd.DataFrame(stats)
stats_df.set_index("trait", inplace=True)
stats_df.to_csv(PERSONALITY_STATS_FILE_PATH)

# Bin personality traits for graph creation
binned_scores = []
for trait in ITEM_TO_TRAIT:
	key = "binned_%s" % trait
	personality_df[key] = pd.cut(personality_df[trait], BINS)

	temp_binned_scores = personality_df[key].value_counts().to_dict()
	temp_binned_scores['trait'] = trait

	binned_scores.append(temp_binned_scores)
binned_scores_df = pd.DataFrame(binned_scores)
binned_scores_df.set_index("trait", inplace=True)
binned_scores_df = binned_scores_df.reindex(sorted(binned_scores_df.columns), axis=1)
binned_scores_df.to_csv(PERSONALITY_BINS_FILE_PATH)

# Get correlation between each personality trait
personality_df[[x for x in ITEM_TO_TRAIT]].corr().to_csv(PERSONALITY_COOR_FILE_PATH)

# Clean / fix individual answers to each question
# Focus on answer string
personality_df = personality_df['Answers']

# Split string and convert to number type
personality_df = personality_df.str.split("-", expand=True)
personality_df = personality_df.astype(int)

# Properly name headers as "item_x", where x is a number from 1 to 44 
# Numbers correspond to each of the 44 items in the BFI
rename_dict = {}
for num in range(1,45):
	rename_dict[num-1] = "item_%d" % num
personality_df.rename(columns=rename_dict, inplace=True)

# Process reverse scores (e.g. 5 --> 1, 2 --> 4)
# See BFI-44 manual for more details
for score in SCORES_TO_REVERSE:
	key = "item_%d" % (score)
	personality_df[key] = personality_df[key].apply(reverse_score)

# Save individual answers to a CSV file
personality_df.to_csv(PERSONALITY_ITEM_SCORES_FILE_PATH, encoding='utf-8')

# Generate Cronbach's Alpha for each dimension
alpha_coefs = []
for trait in ITEM_TO_TRAIT:
	trait_df = personality_df[["item_%s" % x for x in ITEM_TO_TRAIT[trait]]]

	alpha_coefs.append([trait, cronbach_alpha(trait_df)])

# Generate DataFrame of alpha coefficients and save to CSV
pd.DataFrame(alpha_coefs, columns=["Trait", "Cronbach's Alpha"]).to_csv(PERSONALITY_CRONBACHS_ALPHA_FILE_PATH)
from scipy.spatial import distance
import pandas  as pd
import numpy as np


def get_unique(lables_series):
	return lables_series.drop_duplicates()

def generate_matrix(lables):
	from itertools import combinations
	from nltk.metrics.distance import jaccard_distance
	unique_lables = get_unique(lables)
	jaccard_generator = (jaccard_distance(set(tag1.split()), set(tag2.split())) for tag1, tag2 in combinations(lables, r=2))
	flattened_matrix = np.fromiter(jaccard_generator, dtype=np.float64)
	normal_matrix = distance.squareform(flattened_matrix)
	normal_matrix += np.identity(len(tags))
	return normal_matrix



def get_clustering(lables, threshold = 0.5, iteration = 1):
	normal_matrix = generate_matrix(lables)
	filtered_array = np.where(normal_matrix < threshold)
	pairs = (zip(*filtered_array))
	array_list = []

	for i in pairs:
		array_list.append(i)
	df = pd.DataFrame(array_list, columns = ['first_col', 'second_col'])
	grouped_df = df.groupby('first_col')['second_col'].apply(lambda x: list(x))
	new_vec = grouped_df.reset_index()

	for e,k in zip(new_vec.first_col, new_vec.second_col):
		k.append(e)

	second_col = new_vec.second_col
	cluster_df = second_col.apply(lambda x : frozenset(x)).drop_duplicates().reset_index(drop=True)
	return cluster_df


	

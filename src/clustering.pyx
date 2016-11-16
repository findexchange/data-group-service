from scipy.spatial import distance
import pandas as pd
import numpy as np
from collections import defaultdict
cimport numpy as np
cimport cython
from collections import Counter


@cython.boundscheck(False)
@cython.wraparound(False)
cdef double _jaccard(set set1, set set2):
	cdef set interset
	cdef long intersection_len, union_len
	interset = set1.intersection(set2)
	intersection_len = len(interset)
	union_len = len(set1) + len(set2) - intersection_len
	return 1 - float(intersection_len)/float(union_len)

	

def get_tags(data):
	tags = data.tags.drop_duplicates().reset_index(drop = True)
	return tags

def generated_matrix(data):
	tags  = get_tags(data)
	from itertools import combinations
	# cdef np.ndarray 
	jaccard_generator = np.array([_jaccard(set(tag1.split()), set(tag2.split())) for tag1, tag2 in combinations(tags, r=2)])
	flattened_matrix = np.fromiter(jaccard_generator, dtype=np.float64)
	normal_matrix = distance.squareform(flattened_matrix)
	normal_matrix += np.identity(len(tags))
	return normal_matrix


def _seperate_to_cols(list_string):
	return pd.Series(list_string)	



def get_hirachy(data,threshold = 0.5):
	matrix = generated_matrix(data)
	
	tags = get_tags(data)
	
	l = np.where(matrix < threshold)
	pairs = zip(*l)
	array = []
	for i in pairs:
		array.append(i)

	test_d = pd.DataFrame(array, columns = ['first_col', 'second_col'])
	
	grouped = test_d.groupby('first_col')['second_col'].apply(lambda x: list(x)).reset_index()

	for e,k in zip(grouped.first_col, grouped.second_col):
		k.append(e)

	t = grouped.second_col
	t = t.apply(lambda x: frozenset(x)).drop_duplicates().reset_index(drop = True)	
	t = t.apply(lambda x : list(x))

	
	dicti = defaultdict(list)

	for i in t:
		for index in i:
			dicti[i[0]].append(tags[index])
	
	df = pd.DataFrame(pd.Series(dicti).reset_index(drop = True)).rename(columns = {0: 'group'})

	tttt = df.group.apply(_seperate_to_cols)
	tttt = tttt.apply(lambda x: x.fillna(x[0]),axis=1)#.applymap(lambda x: list(x.split()),axis = 1)
	def _getclean_group(glist):
		eee = []
		for i in glist:
			eee.extend(i)
		dd = Counter(eee)
		ddd = {k: v for k, v in dd.iteritems() if v >= len(tttt.columns)-1}
		return ddd.keys()
	refined_tags = tttt.apply(_getclean_group, axis = 1)
	
	ordered_columns = tttt.loc[:,0]
	
	ddf = pd.concat([pd.DataFrame(ordered_columns, columns=['names']),pd.DataFrame(refined_tags, columns=['intersect']).apply(lambda x: list(x), axis=0)], axis =1, join_axes=[pd.DataFrame(ordered_columns).index])
	
	diclst = defaultdict(list)
	for m, k, i in zip(ddf.index,ddf.names, ddf.intersect):
			diclst[m].append({i[l]: k.index(i[l]) for l in range(len(i))})

	dddf = pd.DataFrame(pd.Series(diclst), columns= ['postional'])
	
	dddf.postional= dddf.postional.apply(lambda x : x[0]).apply(lambda x : sorted(x.keys() ,key = x.get)).apply(lambda x: ' '.join(x))        
	new_d = df.join(dddf)

	g = []
	for i in t.tolist():
		g.extend(i)

	index_col = pd.Series(g)

	targets_index = index_col.drop_duplicates().reset_index(drop = True)
	shrinked_tags = tags.loc[targets_index]

	from itertools import product

	results_dict = dict()
	for i, k in product(shrinked_tags,new_d.group):
		if i in k:
			results_dict[i]  = k
	new_a = pd.Series(results_dict).reset_index().rename(columns = {0: 'group'})
	new_a.group = new_a.group.apply(lambda x:frozenset(x))
	new_d.group = new_d.group.apply(lambda x: frozenset(x))

	merged_data = new_a.merge(new_d, on = 'group', how = 'inner')
	merged_data.rename(columns={'index': 'tags'}, inplace= True)

	merged_data.drop('group', inplace= True, axis = 1)



	test = merged_data.to_dict(orient= 'split')['data']

	new_test = dict()
	for i, k in test:
		new_test[i] = k
	
	# data = data
	data['positional'] = data.tags.map(new_test)
	data.positional = data.positional.fillna(data.tags)
	data = data.drop(['tags'], axis = 1).rename(columns = {'positional': 'tags'})

	return data
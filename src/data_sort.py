import pandas as pd
from collections import Counter
import re
import json
import numpy as np

def threaded(fn):
	def wrapper(*args, **kwargs):
		threading.Thread(target=fn, args=args, kwargs=kwargs).start()
	return wrapper

class data_sort:



	def __init__(self, data):
		self.data = data
		self.all_data_df = self.aggreate_all()


	def read_data(self):
		if self.data[-3:] == 'csv':
			data = pd.read_csv(self.data)
		
		elif self.data[-4:] == 'json':
			data = pd.read_json(self.data)
		else:
			print 'please use data format in json or csv'
			data =pd.read_json('./sample_input.json')
		return data

	@staticmethod
	def encode_data(strings):
		strings  = strings.decode('unicode_escape').encode('ascii', 'ignore') 
		return strings

	@staticmethod	
	def lower_clean_suffix(strings):
			strings = strings.lower()
			pattern = re.compile(r'-\s[\w\s]+')
			strings = pattern.sub('', strings).strip()
			pattern2 = re.compile(r'-\s#[\d]+')
			strings = pattern2.sub('',strings).strip()
			pattern3 = re.compile(r'\([\d]+\)')
			strings = pattern3.sub('',strings).strip()
			return strings
	@staticmethod		
	def replace_no_char(strings):
			strings = strings.replace('- ', '')
			strings = strings.replace('&', '')
			strings = strings.replace('(', '')
			strings = strings.replace(')',"")
			pattern = re.compile(r'#[a-z0-9]*')
			strings = pattern.sub('', strings).strip()
			return strings	    


	@staticmethod		
	def add_break(strings):
		strings = '<s>'+ strings + '</s>'
		return strings	    

	
	def get_names(self):
		dataframe = self.read_data()
		dataframe['name'] = dataframe['name'].apply(self.encode_data)
		dataframe['name'] = dataframe['name'].apply(self.lower_clean_suffix)
		dataframe['name'] = dataframe['name'].apply(self.replace_no_char)
		dataframe['name'] = dataframe['name'].apply(self.add_break)
		return dataframe['name']


	@staticmethod	
	def one_word_list(series):
			all_list = []
			for data in series:
				for i in data.split(' '):
					if i == '': pass
					else:
						 all_list.append(i)
			return all_list
			

	@staticmethod		
	def get_ngram(input,n):
		return zip(*[input[i:] for i in range(n)])	     

	
	@staticmethod	
	def delete_nonsense(count_dict):
		for items in count_dict.keys():
				patn = '<s>'+'[\w]+\-'*(len(items)-1) + '[\w]+</s>'
				i = '-'.join(items)
				pattern = re.compile(patn)
				if not pattern.match(i):
					item = tuple(i.split('-'))
					del count_dict[item]
		return count_dict

	@staticmethod
	def tranformations(strings):
		strings = ' '.join(strings)
		strings = strings.replace('<s>','')
		strings = strings.replace('</s>','')
		strings = strings.strip()
		strings = str(strings)
		return strings    


	def aggreate_all(self, n = 2):
		name_series = self.get_names()
		one_word = self.one_word_list(name_series)
		unigrams = self.delete_nonsense(Counter(self.get_ngram(one_word,1)))
		bigrams = self.delete_nonsense(Counter(self.get_ngram(one_word,2)))
		trigrams = self.delete_nonsense(Counter(self.get_ngram(one_word, 3)))
		data_uni = pd.DataFrame(unigrams.items(),columns=['name', 'frequency'])
		data_bi = pd.DataFrame(bigrams.items(), columns = ['name', 'frequency'])
		data_tri = pd.DataFrame(trigrams.items(), columns = ['name', 'frequency'])
		data_uni['name'] = data_uni['name'].apply(self.tranformations)
		data_bi['name'] = data_bi['name'].apply(self.tranformations)
		data_tri['name'] = data_tri['name'].apply(self.tranformations)
		name_uni = data_uni.name[data_uni.frequency >= 2]
		name_bi = data_bi.name

		for shorter_name in name_uni:
			check = shorter_name
			if np.any(data_bi[name_bi.str.contains(check)]['name'] != pd.Series.empty):
				data_bi.loc[name_bi.str.contains(check),'name'] = check
		# results_index.extend(data_bi[name_bi.str.contains(check)]['name'].index)

		
		# data_bi.name = name_bi
		all_data_df = pd.concat([data_uni, data_bi, data_tri])
		all_data_df = all_data_df.groupby('name')['frequency'].sum().reset_index()
		return all_data_df[all_data_df['frequency']>n].reset_index().drop(['index'], axis = 1)


	def tagging(self,target_df):
		for name in self.all_data_df.name:
			check_word = name
			if set(check_word.split()).issubset(set(target_df.split())):
				target_df = check_word
			else:
				target_df = target_df
		return target_df    

	

	def get_tagged(self):
		data = self.read_data()
		# all_data_df = self.aggreate_all()
		data['tags'] =  data.name.apply(self.tagging)
		return data #.to_json(orient = 'records')


	def group_by_tag(self):
		data = self.get_tagged()
		new_data1 = data.groupby('tags')['_id'].apply(lambda x: '[%s]' % ','.join(x)).reset_index()
		new_data2 = data.groupby('tags').count().reset_index().drop(['_id'], axis = 1).rename(columns = {'name':'Count'})
		combined_output = pd.merge(new_data1, new_data2, on = 'tags').rename(columns={'_id':'rows'})
		combined_output.index.name = 'GroupName_id'
		combined_output.reset_index(inplace = True)
		return combined_output.to_json(orient = 'records')




# f = '../../findex-extracted-data.csv'
f = '../../flaskapp/sample_input.json'
test = data_sort(f)
test.get_tagged().to_csv('test_results.csv')
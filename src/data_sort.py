import pandas as pd
from collections import Counter
import re
import json
import numpy as np


class data_sort:

	def __init__(self, data):
		self.data = data
		self.all_data_df = self.aggreate_all()

	def read_data(self):
		try:
			data = pd.read_json(self.data)
		except(ValueError):
			print 'please use data format in Json'
			data = ''
		return data

	#encoding for different langugages	
	@staticmethod
	def encode_data(strings):
		strings  = strings.encode('ascii', 'ignore') 
		return strings

	#put word in lowercase and clean any suffix	
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

	#Clean non-characters		
	@staticmethod		
	def replace_no_char(strings):
		strings = strings.replace('- ', '')
		strings = strings.replace('&', '')
		strings = strings.replace('(', '')
		strings = strings.replace(')',"")
		pattern = re.compile(r'#[a-z0-9]*')
		strings = pattern.sub('', strings).strip()
		return strings	    

	#Add begin and end mark to each name.e.g <s></s>
	@staticmethod		
	def add_break(strings):
		strings = '<s>'+ strings + '</s>'
		return strings	    

	#return cleaned names
	def get_clean_names(self):
		dataframe = self.read_data()
		dataframe['name'] = dataframe['name'].apply(self.encode_data)
		dataframe['name'] = dataframe['name'].apply(self.lower_clean_suffix)
		dataframe['name'] = dataframe['name'].apply(self.replace_no_char)
		dataframe['name'] = dataframe['name'].apply(self.add_break)
		return dataframe['name']


	#break down all the names in to a list
	@staticmethod	
	def one_word_list(series):
			all_list = []
			for data in series:
				for i in data.split(' '):
					if i == '': pass
					else:
						 all_list.append(i)
			return all_list
			
	#N-grams generator	
	@staticmethod		
	def get_ngram(input,n):
		return zip(*[input[i:] for i in range(n)])	     

	
	#Delete the words that not start and end with <s> word </s>
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


	#remove begin and end marks	
	@staticmethod
	def tranformations(strings):
		strings = ' '.join(strings)
		strings = strings.replace('<s>','')
		strings = strings.replace('</s>','')
		strings = strings.strip()
		strings = str(strings)
		return strings    


	@staticmethod
	def replace_no_char_on_tag(strings):
		strings = strings.replace('-', '')
		strings = strings.replace('.', '')
		strings = strings.replace(',', '')
		strings = strings.replace('\"', '')
		strings = strings.replace('+', '')
		return strings

	@staticmethod
	def place_nan(string):
		if len(string) == 0:
			string = np.nan
		return string

		
	#put all together, return a dataframe with all keywords	that has frequency larger than 2
	#They are treated as tags
	def aggreate_all(self, n = 2):
		name_series = self.get_clean_names()
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
		#Compare one word with two words, if contains one word replace two with one word.
		#This only for one word that have frequence larger than 2.
		for shorter_name in name_uni:
			check = shorter_name
			if np.any(data_bi[name_bi.str.contains(check)]['name'] != pd.Series.empty):
				data_bi.loc[name_bi.str.contains(check),'name'] = check
		
		all_data_df = pd.concat([data_uni, data_bi, data_tri])
		all_data_df = all_data_df.groupby('name')['frequency'].sum().reset_index()
		all_data_df.name = all_data_df.name.apply(self.replace_no_char_on_tag)
		all_data_df.name = all_data_df.name.apply(self.place_nan).dropna()
		all_data_df.name = all_data_df.name.apply(lambda x: str(x))
		#return keyword that has frequency larger than 2
		return all_data_df[all_data_df['frequency']>n].reset_index().drop(['index'], axis = 1)


	#Tag each row with each keywords generated previous
	def tagging(self,target_df):
		for name in self.all_data_df.name:
			check_word = name
			if set(check_word.split()).issubset(set(target_df.split())):
				target_df = check_word
			else:
				target_df = target_df
		return target_df    

	
	#create a column called tags
	def get_tagged(self):
		data = self.read_data()
		data['tags'] =  data.name.apply(self.encode_data).apply(lambda x: x.lower()).apply(self.tagging)
		# data.applymap(self.encode_data).to_csv('results.csv') this line is for local testing 
		return data 


	#Orgnize the results in to required format
	def output_data(self):
		data = self.get_tagged()
		new_data1 = data.groupby('tags')['_id'].apply(lambda x: "%s" % ",".join(x).split(",")).reset_index()
		new_data2 = data.groupby('tags').count().reset_index().drop(['_id'], axis = 1).rename(columns = {'name':'count'})
		combined_output = pd.merge(new_data1, new_data2, on = 'tags').rename(columns={'_id':'rows'})
		combined_output.index.name = 'groupName_Id'
		combined_output.reset_index(inplace = True)
		return json.dumps(combined_output.to_json(orient = 'records').replace('"[',"[").replace(']"',']'))









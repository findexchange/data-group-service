import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from src import flask_app
from src import data_sort
import unittest


class FlaskrTestCase(unittest.TestCase):
	
	def setUp(self):
		flask_app.app.config['TESTING'] = True
		self.app = flask_app.app.test_client()
		self.data_sort = data_sort
		self.file = os.path.join(os.path.dirname(__file__),'./sample_input.json')


	#Test input data type and check response code
	def test_data_type(self):
		result = self.app.post('/api/v1.0/datasort', data= self.file)
		print 'Testing data type in the foramt of json.'
		self.assertEqual(result.status_code, 200)


	#Testing whether counts are corret for each group 
	#And return total number of groups
	def test_num_in_each_group(self):
		upload_data = self.app.post('/api/v1.0/datasort', data= self.file)
		print 'Comparing the number in groups with count column.'
		import json
		data = upload_data.data
		result = json.loads(data)['results']
		print 'There are :' ,len(result), 'of group generated.'
		import pandas as pd
		data_frame = pd.read_json(json.dumps(result))
		count = data_frame['count']
		rows = data_frame['rows']
		count_ids_rows = rows.apply(lambda x: str(x)).apply(lambda x : x.strip('[]').split(',')).apply(lambda x: len(x))
		data_frame['no_in_group'] = count_ids_rows
		compare_with_count =  data_frame[~data_frame['count'] == data_frame['no_in_group']]
		self.assertEqual(len(compare_with_count),0)


if __name__ == '__main__':
	unittest.main()

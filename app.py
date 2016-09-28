from flask import Flask,jsonify
from flask import request
from flask import abort
from data_sort import data_sort

app = Flask(__name__)


@app.route('/app/v1.0/return', methods = ['GET'])

def get_clean_data():
	data_tasks = test.group_by_tag()
	return jsonify({'tasks': data_tasks})



@app.route('/app/v1.0/upload', methods = ['post'])
def input_data():
	global test


	f = request.get_json()
	if f is not request.json:
		abort(404)
	test = data_sort(f)
	t = len(f)
	return jsonify({'task': t}), 201



if __name__ == '__main__':
	app.run(debug = True)
from flask import Flask
from flask import request
from flask import jsonify
from data_sort import data_sort

app = Flask(__name__)


@app.route('/app/v1.0/upload', methods = ['POST','GET'])
def input_data():
	import json

	data = json.dumps(request.data)
	start_sorting = data_sort(data)
	results = start_sorting.group_by_tag()
	return jsonify({'results': results}), 201


if __name__ == '__main__':
	app.run(debug = True)



#curl -i -H "Content-Type: application/json"  -X POST http://127.0.0.1:5000/app/v1.0/upload -d @sample_input.json
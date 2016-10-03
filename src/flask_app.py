from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from data_sort import data_sort
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)


#Post json data 
@app.route('/app/v1.0/datasort', methods = ['POST'])
def input_data():
	try:
		data = request.data
		start_sorting = data_sort(data)
		results = start_sorting.output_data()

	except(ValueError):
		results = "No results sent"

	return results, 200


#Page not found
@app.errorhandler(404)
def not_found(exception):
	return make_response(jsonify({'Error': 'Page not found'}), 404)


#Internal Error
@app.errorhandler(500)
def server_error(exception):
	return make_response(jsonify({'Error': "Internal Server Error"}), 500)



if __name__ == '__main__':
	#Rotating saving logs into file wi maxbytes = 10000, backupCount up to 10
	#The logging file will be save in the same directory
	handler = RotatingFileHandler('logging_info.log', maxBytes = 10*1024*1024, backupCount = 10)
	#Level set as INFO
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	handler.setFormatter(formatter)
	app.logger.info('Data sorting services is running')
	app.logger.addHandler(handler)
	app.run()
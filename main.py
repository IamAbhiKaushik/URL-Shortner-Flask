from flask import Flask, abort, request, redirect
from pymongo import MongoClient
import string
import random
from bson.json_util import dumps
from datetime import datetime

app = Flask(__name__)
# mongo = MongoClient('mongodb://mongo/test').db
mongo = MongoClient('mongodb://localhost:27017').db
BASE_URL = "http://localhost:5000"

@app.route("/")
def home():
	# return dumps({'Version': 1.2, 'health': 'Working Fine'})
	return dumps(mongo.record_table.find())

# @app.route('/api/minify_post_api', methods=['GET', 'POST']) #allow both GET and POST requests
# def minify_post_api():
# 	if request.method == "POST":
# 		original_url = request.form.get('original_url')
# 		is_custom = request.form['is_custom']
# 		return '''<h1>The language value is: {}</h1>
#                   <h1>The framework value is: {}</h1>'''.format(original_url, is_custom)

# 		# return "Submitted the form"
# 	else:
# 	    return '''<form method="POST">
# 	                  Language: <input type="text" name="original_url"><br>
# 	                  Framework: <input type="text" name="is_custom"><br>
# 	                  <input type="submit" value="Submit"><br>
# 	              </form>'''



@app.route('/api/minify', methods=['POST']) #allow POST requests with header 'application/json type input'
def minify():
	request_data = request.get_json()
	# if vaildate_request_data(request_data):
		# redirect_url = request_data['redirect_url']
	if "custom_url" in request_data:
		custom_url = request_data['custom_url']
		previous_record = mongo.record_table.find_one({"custom_url": custom_url})
		if not previous_record and (4 <=len(custom_url) <= 8):
			insert_response = mongo.record_table.insert_one({
				"createdAt": datetime.utcnow(),
				'original_url': request_data['original_url'],
				'custom_url': request_data['custom_url'],
				'visits': 0
				})
			response = mongo.record_table.find_one({"_id": insert_response.inserted_id})
		else:
			if previous_record:
				return dumps({'error': 'Custom url already in use, Please try something'})
			return dumps({'error': 'Custom url should be of length 4 to 8 only.'})
	else:
		custom_url = id_generator()
		insert_response = mongo.record_table.insert_one({
			"createdAt": datetime.utcnow(),
			'original_url': request_data['original_url'],
			'custom_url': custom_url,
			'visits': 0
			})
		# mongo.record_table.update({'_id': insert_response.inserted_id}, {'custom_url': custom_url})
		response = mongo.record_table.find_one({"custom_url": custom_url})
	return dumps(response)



# @app.route("/add_url")
# def add_url():
# 	custom_url = id_generator()
# 	insert_response = mongo.record_table.insert_one({
# 		"createdAt": datetime.utcnow(),
# 		'original_url': "google.com",
# 		'custom_url': custom_url,
# 		'visits': 0
# 		})
# 	# mongo.record_table.update({'_id': insert_response.inserted_id}, {'custom_url': custom_url})
# 	response = mongo.record_table.find_one({"custom_url": custom_url})
# 	return dumps(response)

# @app.route("/find_url")
# def find_url():
# 	url_collection = mongo.record_table
# 	url = url_collection.find_one({"key": "abcd"})
# 	return f"Redirecting to URL: {url['original_url']}"


@app.route('/<custom_url>', methods=['GET'])
def redirect_to_url(custom_url):
	response = mongo.record_table.find_one({"custom_url": custom_url})
	if response:
		response['visits'] = int(response['visits'])+1
		mongo.record_table.update({'custom_url': response['custom_url']}, response)
		# return redirect(response['original_url'])
		return dumps(response)
	else:
		return redirect(BASE_URL)


@app.route('/visits/<custom_url>', methods=['GET'])
def custom_url_visits(custom_url):
	response = mongo.record_table.find_one({'custom_url':custom_url})
	if response:
		return dumps(response)
		# mongo.record_table.update({'custom_url': response['custom_url']}, {'visits': int(response['visits']+1)})
	else:
		return custom_url + " not found in Mongo Database"




def id_to_short_url(response_id):
	string_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	while response_id:
		short_url += string_set[response_id%62]
		response_id = response_id/62
	return short_url


def id_generator(size=6, chars=string.ascii_uppercase+ string.ascii_lowercase + string.digits):
	custom_url = ''.join(random.choice(chars) for _ in range(size))
	previous_record = mongo.record_table.find_one({"custom_url": custom_url})
	if not previous_record:
		return custom_url

	return id_generator()

def setup_database():
	mongo.record_table.ensure_index("createdAt", expireAfterSeconds=60)       
	mongo.record_table.create_index("custom_url")
	# pass

# "createdAt": datetime.datetime.now(),

if __name__ == "__main__":
	# setup_database()
	app.run(debug=True, host='0.0.0.0')


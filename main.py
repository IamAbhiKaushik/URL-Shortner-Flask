from flask import Flask, abort, request
import json
# from flask_pymongo import PyMongo
from pymongo import MongoClient
import string
import random
# import requests
app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/admin"
# mongo = MongoClient('mongodb://mongo/test')
mongo = MongoClient('mongodb://localhost:27017').db
BASE_URL = "http://localhost:5000"
@app.route("/")
def home():
	return "This is THe K MR K page of our website"
    
# @app.route("/api/minify", methods=['POST'])
# def minify():
	# if not request.json or not 'redirect_url' in request.json:
		# abort(400)
	# redirect_url = request["redirect_url"]
	# task = {
	# "redirect_url": request.json["redirect_url"],
	# redirect_url= "This is redirect_url"
	# "custom_url": "abcd"
	# }
    # task ={'title': request.json['title'], 'description': request.json.get('description', "No new description"), 'done': "True"}
    # custom_url = "abcd"
	# return request


@app.route('/api/minify_post_api', methods=['GET', 'POST']) #allow both GET and POST requests
def minify_post_api():
	if request.method == "POST":
		redirect_url = request.form.get('redirect_url')
		is_custom = request.form['is_custom']
		return '''<h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(redirect_url, is_custom)

		# return "Submitted the form"
	else:
	    return '''<form method="POST">
	                  Language: <input type="text" name="redirect_url"><br>
	                  Framework: <input type="text" name="is_custom"><br>
	                  <input type="submit" value="Submit"><br>
	              </form>'''



@app.route('/api/minify', methods=['POST']) #allow POST requests with header 'application/json type input'
def minify():
	request_data = request.get_json()
	if vaildate_request_data(request_data):
		# redirect_url = request_data['redirect_url']
		# if "is_custom" in request_data:
		if request_data['is_custom'] == "true":
			insert_response = mongo.mapurls.insert_one({
				'redirect_url': request_data['redirect_url'],
				'is_custom': request_data['is_custom'],
				'custom_url': request_data['custom_url']
				})
			response = mongo.mapurls.find_one({"_id": insert_response.inserted_id})
		else:
			insert_response = mongo.mapurls.insert_one({
				'redirect_url': request_data['redirect_url'],
				'is_custom': request_data['is_custom']
				})
			custom_url = id_generator()
			mongo.mapurls.update({'_id': insert_response.inserted_id}, {'custom_url': custom_url})
			response = mongo.mapurls.find_one({"custom_url": custom_url})
		hash_value = convert_to_short_url(response)
		return hash_value



@app.route("/add_url")
def add_url():
	# db = mongo.db
	# url_maping = mongo.db.mapurls
	url_maping.insert({ "key":"abcd", "redirect_url":"google.com", "custom":True, "visits": 10})
	return "New URL Added in table"

@app.route("/find_url")
def find_url():
	url_collection = mongo.db.mapurls
	url = url_collection.find_one({"key": "abcd"})

	return f"Redirecting to URL: {url['redirect_url']}"

def id_to_short_url(response_id):
	# response_id = int(response_id)
	string_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	
	# short_url = 
	while response_id:
		short_url += string_set[response_id%62]
		response_id = response_id/62
	return short_url

def vaildate_request_data(request_data):
	return True

def convert_to_short_url(response):
	# return response
	l = [str(response[key])+str(key) for key in response]
	return '-'.join(l)
	# for key in response:

	# l = []
	# for record in response:
		# l.append(record['_id'])
	# return f"This is so sed {response['_id']}"


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
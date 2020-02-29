from flask import Flask
import json
# from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/admin"
mongo = MongoClient('mongodb://mongo/test')

@app.route("/")
def home():

	return "This is THe Kaushik page of our website"
    


@app.route("/add_url")
def add_url():
	# db = mongo.db
	url_maping = mongo.db.mapurls
	url_maping.insert({ "key":"abcd", "redirect_url":"google.com", "custom":True, "visits": 10})
	return "New URL Added in table"

@app.route("/find_url")
def find_url():
	url_collection = mongo.db.mapurls
	url = url_collection.find_one({"key": "abcd"})

	return f"Redirecting to URL: {url['redirect_url']}"



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
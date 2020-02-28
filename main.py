from flask import Flask
import json

app = Flask(__name__)

@app.route("/")
def home():
	a = {
		"name": "Abhinav",
		"class": 10,
		"objective": True
	}
	return json.dumps(a)
    


@app.route("/fetch_url")
def fetch_url():
	return "URL TO BE TRANSFERED"

if __name__ == "__main__":
    app.run(debug=True, host='')
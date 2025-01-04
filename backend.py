from flask import Flask, render_template, jsonify
import subprocess
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client['twitter_trends']
collection = db['trending_topics']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-script", methods=["GET"])
def run_script():
    try:
        # Run the Selenium script
        record = subprocess.check_output(["python", "selenium_script.py"])
        return jsonify(record.decode())
    except Exception as e:
        return str(e)

@app.route("/latest-record", methods=["GET"])
def latest_record():
    record = collection.find().sort("timestamp", -1).limit(1)[0]
    return jsonify(record)

if __name__ == "__main__":
    app.run(debug=True)

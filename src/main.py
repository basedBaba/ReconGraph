from flask import Flask, jsonify, request
import requests

app = Flask(__name__)



@app.route('/')
def home():
    return "Welcome to the ReconGraph!"



if __name__ == "__main__":
    app.run(debug=True)

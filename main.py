from flask import Flask
from flask_restful import Resource, Api
import json

app = Flask(__name__);

@app.route("/")
def main():
  return "main page"

@app.route("/loadData", methods=["GET", "POST"])
def loadData():
 return "load"

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5009)
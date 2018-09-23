from flask import Flask, request, jsonify
import json

from module.ktis import KTIS
app = Flask(__name__);

@app.route("/")
def main():
  return "main page"

@app.route("/ktis/toDB", methods=["GET", "POST"])
def KTIStoDB():
  if request.method == 'POST':
    data = request.json
    return KTIS.ToDB(data)
  else:
    return "POST id and pw"

@app.route("/ktis/login", methods=["GET", "POST"])
def KTISlogin():
  if request.method == 'POST':
    data = request.json
    return KTIS.Login(data)
  else:
    return "POST id and pw"

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5009)
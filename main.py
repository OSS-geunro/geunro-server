from flask import Flask, request, jsonify
import json

from module.ktis import GetTimetable

app = Flask(__name__);

@app.route("/")
def main():
  return "main page"

@app.route("/loadData", methods=["GET", "POST"])
def loadData():
  if request.method == 'POST':
    data = request.json
    timetable = GetTimetable(data)
    return jsonify(timetable)
  else:
    return "POST id and pw"

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5009)
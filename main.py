from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json

from module.ktis import KTIS
from module.worktable import Worktable
from module.timetable import Timetable

app = Flask(__name__);
CORS(app)

@app.route("/")
def main():
  return "main page"

@app.route("/api/ktis/toDB", methods=["POST"])
def KTIStoDB():
  if request.method == 'POST':
    data = request.form
    data = data.to_dict()

    response = Response(
        status=int(KTIS.ToDB(data)),
        mimetype='application/json'
    )
    return response
  else:
    return "POST id and pw"

# POST
# {
#     "id" : " ",
#     "pw" : " "
# }

@app.route("/api/ktis/login", methods=["GET", "POST"])
def KTISlogin():
  if request.method == 'POST':
    data = request.json

    response = Response(
        status=int(KTIS.Login(data)),
        mimetype='application/json'
    )
    return response
  else:
    return "POST id and pw"

# POST
# {
#     "id" : " ",
#     "pw" : " "
# }

@app.route("/api/work/add", methods=["POST"])
def WorkAdd():
  print("dddd")
  if request.method == 'POST':
    data = request.json
    return Worktable.CreateWork(data)
    print("sss")
  else:
    return "POST worktable, name, day, start, end and minimum"

# POST
# {
#     "worktable" : " ",
#     "name" : " ",
#     "day" : " ",
#     "start" : " ",
#     "end" : " ",
#     "minimum" : " "
# }

@app.route("/api/work/create", methods=["GET", "POST"])
def WorkCreate():
  if request.method == 'POST':
    data = request.json
    return Worktable.Update(data)
  else:
    return "POST worktable,daily and weekly"

# POST
# {
#     "worktable" : " ",
#     "daily" : " ",
#     "weekly" : " "
# }

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5009)
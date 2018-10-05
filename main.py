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

#시간표 업로드
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

#로그인
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

#근로시간표 제작
@app.route("/api/work/add", methods=["POST"])
def WorkAdd():
  if request.method == 'POST':
    IDs = request.form.getlist("IDs[]")
    events = json.loads(request.form.getlist("events")[0])
    worktable = request.form.getlist("worktable")
    response = Response(
        status = int(Worktable.CreateWork(IDs, events, worktable)),
        mimetype ='application/json'
    )
    return response
  else:
    return "POST worktable(name, day, start, end, minimum)"

# POST
# {
#     "worktable" : " ",
#     "name" : " ",
#     "day" : " ",
#     "start" : " ",
#     "end" : " ",
#     "minimum" : " "
# }


@app.route("/api/work/getlist", methods=["GET"])
def WorkList():
  if request.method == 'GET':
    response = Response(
        response = Worktable.GetList(),
        status = 200,
        mimetype ='application/json'
    )
    return response
  else:
    return "GET WorkTable list"



@app.route("/api/work/getid", methods=["POST"])
def WorkCreate():
  if request.method == 'POST':
    data = request.form
    response = Response(
        response = Worktable.Update(data),
        status = 200,
        mimetype ='application/json'
    )
    return response
  else:
    return "POST workTable ID"


@app.route("/api/work/access", methods=["POST"])
def WorkAccess():
  if request.method == 'POST':
    data = request.form
    response = Response(
        response = Worktable.Access(data),
        status = 200,
        mimetype ='application/json'
    )
    return response
  else:
    return "POST WorkTable ID"

@app.route("/api/work/delete", methods=["POST"])
def DeleteTable():
  if request.method == 'POST':
    data = request.form
    response = Response(
        response = Worktable.DelTable(data),
        status = 200,
        mimetype ='application/json'
    )
    return response
  else:
    return "POST WorkTable ID"


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5009)
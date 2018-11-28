from flask import Flask, request, jsonify, Response, render_template, session, redirect, url_for
from flask_cors import CORS
import json

from module.ktis import KTIS
from module.worktable import Worktable
from module.timetable import Timetable

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
CORS(app)


@app.route("/login", methods=["GET", "POST"])
def main():
    if request.method == 'POST':
        result = int(KTIS.Login(request))
        if result is 200:
            session['id'] = request.form['id']
            session['userType'] = request.form['radio']
        response = Response(
            status=result,
            mimetype='application/json'
        )
        return response
    elif 'id' in session:
        print(session['userType'])
        if session['id'] == "student":
            return redirect(url_for('studentTable'))
        else:
            return redirect(url_for('teacherTable'))
    else:
        return render_template('login.html')


@app.route("/student")
def studentTable():
    if 'id' in session:
        exist = Worktable.GetList("111")
        return render_template('student-table.html', exist=exist)
    else:
        return redirect(url_for('main'))


@app.route("/apply", methods=["GET", "POST"])
def studentApply():
    if request.method == 'POST':
        result = int(KTIS.ToDB(request, session["id"]))
        response = Response(
            status=result,
            mimetype='application/json'
        )
        return response
    elif 'id' in session:
        return render_template('apply.html', id=session["id"])
    else:
        return redirect(url_for('main'))


@app.route("/teacher")
def teacherTable():
    if 'id' in session:
        exist = Worktable.GetList("111")
        return render_template('teacher-table.html', exist=exist)
    else:
        return redirect(url_for('main'))


@app.route("/create", methods=["GET", "POST"])
def teacherCreate():
    if request.method == 'POST':
        # result = int(KTIS.ToDB(request, session["id"]))
        print(request)
        response = Response(
            status=200,
            mimetype='application/json'
        )

        return response
    elif 'id' in session:
        return render_template('create.html', id=session["id"])
    else:
        return redirect(url_for('main'))


@app.route('/logout')
def logout():
        # remove the username from the session if its there
    session.pop('id', None)
    session.pop('userType', None)
    return redirect(url_for('main'))


# 근로시간표 제작
@app.route("/api/work/add", methods=["POST"])
def WorkAdd():
    if request.method == 'POST':
        IDs = request.form.getlist("IDs[]")
        events = json.loads(request.form.getlist("events")[0])
        worktable = request.form.getlist("worktable")
        response = Response(
            status=int(Worktable.CreateWork(IDs, events, worktable)),
            mimetype='application/json'
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
            response=Worktable.GetList(),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        return "GET WorkTable list"


@app.route("/api/work/getid", methods=["POST"])
def WorkCreate():
    if request.method == 'POST':
        data = request.form
        response = Response(
            response=Worktable.Update(data),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        return "POST workTable ID"


@app.route("/api/work/access", methods=["POST"])
def WorkAccess():
    if request.method == 'POST':
        data = request.form
        response = Response(
            response=Worktable.Access(data),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        return "POST WorkTable ID"


@app.route("/api/work/delete", methods=["POST"])
def DeleteTable():
    if request.method == 'POST':
        data = request.form
        response = Response(
            response=Worktable.DelTable(data),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        return "POST WorkTable ID"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5009)

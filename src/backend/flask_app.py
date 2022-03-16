import uuid, time, random, json, logging, boto3, base64
from flask import Flask, jsonify, request#, render_template, Response
import ast

from flask_cors import CORS
import pymysql
from DBUtils.PooledDB import PooledDB

app = Flask(__name__)
CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

connection_pool = PooledDB(creator       = pymysql,     # Python function returning a connection or a Python module, both based on DB-API 2
                           host      = 'A.com',
                           user      = 'B',
                           password  = 'C',
                           database  = 'D',
                           autocommit    = False,
                           charset       = "utf8mb4" ,
                           cursorclass   = pymysql.cursors.DictCursor,
                           blocking      = False,
                           maxconnections = 8)

session_duration_minutes = 45
bcount = 20.0
pcount = 20.0
ccount = 20.0

def do_sql(query):
    connection_object = connection_pool.connection()
    cursor = connection_object.cursor()
    cursor.execute(query)
    if query.upper().startswith("SELECT"):
        records = cursor.fetchall()
        cursor.close()
        connection_object.close()
        return records
    elif query.upper().startswith("INSERT"):
        connection_object.commit()
        result_string = "{} records inserted.".format(cursor.rowcount)
        cursor.close()
        connection_object.close()
        return result_string

def questions(answers = True):
    data = {}
    for q in do_sql("SELECT * FROM questions WHERE NOT sub='X';"):
        q["As"] = ast.literal_eval(q["As"].replace('\xa0', ' '))
        if not answers:
            del q["Acorrect"]
        data[str(q["id"])] = q
    return data


@app.route('/login', methods = ["POST"])
def login():
    data = request.get_json()
    if data["pass"].startswith("SECRET"):
        # create user record and return it
        uid = "{}.{}".format(uuid.uuid4().int, time.time())
        thetime = int(time.time())
        timeout = int(thetime + (session_duration_minutes*60) + 600)
        user = {
            "uid": uid,
            "name": data["name"],
            "to": timeout,
            "tn": thetime
        }
        logging.info(do_sql("INSERT INTO users (uid, name, timeout, passcode) VALUES ('{}', '{}', {}, '{}');".format(user["uid"], user["name"], user["to"], data["pass"])))
        return jsonify(user)
    else:
        return ("Invalid access code.", 403)


@app.route('/qs')
def get_questions():
    users = do_sql("SELECT * FROM users WHERE uid = '{}' LIMIT 1;".format(request.headers.get("x-token", "NO_USER_SPECIFIED")))
    if len(users) > 0:
        get_qs = questions(answers=False)
        qs = []
        qlist = list(get_qs)
        random.shuffle(qlist)
        for qkey in qlist:
            q = get_qs[qkey]
            q["qid"] = qkey
            random.shuffle(q["As"])
            As = {}
            i=0
            for a in q["As"]:
                i+=1
                As[qkey+"."+str(i)] = a
            q["As"] = As
            qs.append(q)
        return jsonify(qs)
    else:
        return ("Invalid access header.", 403)


@app.route('/a', methods = ["POST"])
def send_answer():
    users = do_sql("SELECT * FROM users WHERE uid = '{}' LIMIT 1;".format(request.headers.get("x-token", "NO_USER_SPECIFIED")))
    if len(users) > 0:
        for user in users:
            if user["timeout"] > int(time.time()):
                data = request.get_json()["a"].split("#")
                q = data[0]
                a = data[1]
                qs = questions()

                if a == qs[q]["Acorrect"]:
                    correct = True
                else:
                    correct = False

                data = {
                    "uid": user["uid"],
                    "uid1": user["id"],
                    "q": int(q),
                    "a": correct,
                    "ts": int(time.time()),
                    "sub": qs[q]["sub"]
                    }

                connection_object = connection_pool.connection()
                cursor = connection_object.cursor()

                cursor.execute("SELECT * FROM answers WHERE uid1 = {} AND q = {};".format(data["uid1"], q))
                record = cursor.fetchone()

                if record:
                    data["id"] = record["id"]
                    cursor.execute("""
                    UPDATE answers
                    SET uid='{uid}', uid1={uid1}, q={q}, a={a}, ts={ts}, sub='{sub}'
                    WHERE id={id};
                    """.format(**data))
                    connection_object.commit()
                    cursor.close()
                    connection_object.close()
                else:
                    cursor.execute("""
                    INSERT INTO answers
                        (uid, uid1, q, a, ts, sub)
                    VALUES
                        ('{uid}', {uid1}, {q}, {a}, {ts}, '{sub}')
                    """.format(**data))
                    connection_object.commit()
                    cursor.close()
                    connection_object.close()
                return ("", 204)
            else:
                return ("Invalid user session, or session timed out.", 403)
    else:
        return ("Invalid access header.", 403)


@app.route('/res', methods = ["POST"])
def get_results():
    data = request.get_json()
    if data["pass"] == "SECRET":
        results = []

        for user in do_sql("SELECT * FROM users ORDER BY timeout DESC LIMIT 12;"):
            userdata = {
                "name": user["name"],
                "timetaken": 0,
                "B":0,
                "C":0,
                "P":0,
                "id": user["id"]
                }
            start=999999999999
            end=0
            for answer in do_sql("SELECT * FROM answers WHERE uid1 = {};".format(user["id"])):
                if answer["a"]: userdata[answer["sub"]] += 1
                if answer["ts"] > end: end = answer["ts"]
                if answer["ts"] < start: start = answer["ts"]
            userdata["B"] = (float(userdata["B"]) / bcount) * 100.0
            userdata["C"] = (float(userdata["C"]) / ccount) * 100.0
            userdata["P"] = (float(userdata["P"]) / pcount) * 100.0
            userdata["timetaken"] = int(end) - int(start)

            results.append(userdata)

        return jsonify(results)
    else:
        return ("Incorrect passcode", 403)


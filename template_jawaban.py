#6C /19090075 /Nur Khafidah
#6D /19090133 /Helina Putri


# import library
from flask import Flask, make_response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random, string


# Inisialisasi
database_file = 'sqlite:///database/users.db'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# DATABASE
class User(db.Model):
    name = db.Column(db.String(25), unique=False, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(20), unique=False, nullable=False)
    token = db.Column(db.String(100), unique=False)

db.create_all()


# http://127.0.0.1:5000/signUp
@app.route('/signUp', methods=["POST"])
def signUp():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    user = User(name=name, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify({"msg": "Register Completed !"}))

  # http://127.0.0.1:5000/signIn
@app.route('/signIn', methods=["POST"])
def signIn():
    username = request.form.get('username')
    password = request.form.get('password')

    # checking data
    query1 = User.query.filter_by(username=username).first()
    query2 = User.query.filter_by(password=password).first()

    if query1 and query2:
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        User.query.filter_by(username=username).update({'token': token})
        db.session.commit()
        return make_response(jsonify({"msg":"Login Successful !", "token": token}))
    return make_response(jsonify({"msg":"Login failed !"}))

# http://127.0.0.1:5000/api/info_user
@app.route('/api/info_user', methods=["POST"])
def info_user():
    token = request.values.get('token')
    auth = User.query.filter_by(token=token).first()
    if auth:
        dict_users = {"name": auth.name, "username": auth.username, "password": auth.password , "token": auth.token}
        return make_response(jsonify(dict_users))
    return make_response(jsonify({"msg": "Token Invalid !"}))


# http://127.0.0.1:5000/api/allusers
@app.route('/api/allusers', methods=["GET"])
def allUser():
    users = User.query.all()
    array_users = []
    for user in users:
        dict_users = {}
        dict_users.update({"name": user.name, "username": user.username, "password": user.password})
        array_users.append(dict_users)
    return make_response(jsonify(array_users), 200, {'content-type':'application/json'})

if __name__ == '__main__':
   app.run(debug = True, port=5000)
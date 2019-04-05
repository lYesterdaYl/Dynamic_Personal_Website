from flask import Flask, render_template, request, redirect, \
    url_for, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from database_structure import *
import json
import setting
import hashlib
import time, random

import timeit

app = Flask(__name__)

APPLICATION_NAME = "Movie Search App"
app.config['SQLALCHEMY_DATABASE_URI'] = setting.DB_URI
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
session = db.session


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':


        return render_template('result.html')
    else:
        # return "OK"
        return render_template('index.html')


@app.route('/user/create_account', methods=['POST'])
def create_account():
    """
    Create account for users
    :param username: user name
    :param password: user password
    :param gender: user gender(0 for unknown, 1 for male, 2 for female)
    :param age: user age
    :param telephone: user telephone number
    :param country: user country
    :param state: user state
    :param city: user city
    :return:{"msg": "", "code": "200"}
    """
    response = {}
    if request.method == 'POST':
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        gender = request.form.get("gender", "0")
        age = request.form.get("age", 0)
        major = request.form.get("major", "")
        telephone = request.form.get("telephone", "")
        country = request.form.get("country", "")
        state = request.form.get("state", "")
        city = request.form.get("city", "")

        if username == "" or password == "":
            response['msg'] = "Username or Password is empty"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)

        # md5 encryption
        encryption = hashlib.md5()
        encryption.update(password.encode(encoding='utf-8'))
        password = encryption.hexdigest()

        user = session.query(User).filter_by(username=username).first()
        if user is None:
            new_user = User(username=username, password=password, gender=gender, age=age, major=major, telephone=telephone, country=country,
                            state=state, city=city)
            session.add(new_user)
            session.commit()
            response['msg'] = "User Created"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)
        else:
            response['msg'] = "User Already Exist"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)

    else:
        response['msg'] = "Method Not Allowed"
        response['code'] = "200"
        return make_response(json.dumps(response), 405)


@app.route('/user/login', methods=['POST'])
def user_login():
    """
    App login function
    :param username: user name
    :param password: user password
    :return: {"msg": "auth successful", "data": "", "code": "200"}
    """

    response = {}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = session.query(User).filter_by(username=username).first()

        hash = hashlib.md5()
        hash.update(password.encode(encoding='utf-8'))
        if user is None or hash.hexdigest() != user.password:
            response['msg'] = "Wrong username or password"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)
        elif hash.hexdigest() == user.password:
            now = int(time.time())
            session_code = str(now) + str(random.randint(10000, 99999))
            user.session = session_code
            session.add(user)
            session.commit()

            data = {}
            data['id'] = user.id
            data['username'] = user.username
            data['gender'] = user.gender
            data['age'] = user.age
            data['major'] = user.major
            data['telephone'] = user.telephone
            data['country'] = user.country
            data['state'] = user.state
            data['city'] = user.city
            data['country'] = user.country
            data['session'] = user.session

            response['msg'] = "Auth successful"
            response['data'] = data
            response['code'] = "200"
            return make_response(json.dumps(response), 200)
        else:
            response['msg'] = "Unknown Error"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)

    else:
        response['msg'] = "Method Not Allowed"
        response['code'] = "405"
        return make_response(json.dumps(response), 405)


if __name__ == '__main__':
    app.secret_key = "secret_key"
    app.debug = True
    app.run(host='localhost', port=5000)



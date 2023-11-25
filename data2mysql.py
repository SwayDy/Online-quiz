import random

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# MySQL所在的主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号
PORT = 3306
# 连接MySQL的用户名
USERNAME = "root"
# 连接MySQL的密码
PASSWORD = "123456"
# MySQL上创建的数据库名称
DATABASE = "习概题库"

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"

db = SQLAlchemy(app)


class sChoice(db.Model):
    __tablename__ = "sChoice"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500))
    option1 = db.Column(db.String(500))
    option2 = db.Column(db.String(500))
    option3 = db.Column(db.String(500))
    option4 = db.Column(db.String(500))
    answer = db.Column(db.String(10))


class mChoice(db.Model):
    __tablename__ = "mChoice"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500))
    option1 = db.Column(db.String(500))
    option2 = db.Column(db.String(500))
    option3 = db.Column(db.String(500))
    option4 = db.Column(db.String(500))
    answer = db.Column(db.String(10))


class TFChoice(db.Model):
    __tablename__ = "TFChoice"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500))
    answer = db.Column(db.String(10))


with app.app_context():
    db.create_all()

    with open("../sChoice.txt", "r", encoding="utf-8") as f:
        content = f.readlines()

    for ct in content:
        ct = ct.split('xx')
        question = ct[0]
        option1 = ct[1]
        option2 = ct[2]
        option3 = ct[3]
        option4 = ct[4]
        answer = ct[5]
        db.session.add_all([sChoice(question=question, option1=option1, option2=option2,
                                    option3=option3, option4=option4, answer=answer)])

    with open("../mChoice.txt", "r", encoding="utf-8") as f:
        content = f.readlines()

    for ct in content:
        ct = ct.split('xx')
        question = ct[0]
        option1 = ct[1]
        option2 = ct[2]
        option3 = ct[3]
        option4 = ct[4]
        answer = ct[5]
        db.session.add_all([mChoice(question=question, option1=option1, option2=option2,
                                    option3=option3, option4=option4, answer=answer)])

    with open("../TFChoice.txt", "r", encoding="utf-8") as f:
        content = f.readlines()

    for ct in content:
        ct = ct.split('xx')
        question = ct[0]
        answer = ct[1]
        db.session.add_all([TFChoice(question=question, answer=answer)])

    # db.session.commit()

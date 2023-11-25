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


# with app.app_context():
#     db.create_all()

def get_100_questions(numofs=50, numofm=30, numoftf=20):
    schoice = sChoice.query.all()
    mchoice = mChoice.query.all()
    tfchoice = TFChoice.query.all()

    schoice = [{'question': sc.question, 'options': [sc.option1, sc.option2, sc.option3, sc.option4],
                'answer': sc.answer, 'selectedOption': 0} for sc in schoice]
    mchoice = [{'question': mc.question, 'options': [mc.option1, mc.option2, mc.option3, mc.option4],
                'answer': mc.answer, 'selectedOption': 0} for mc in mchoice]
    tfchoice = [{'question': tc.question, 'answer': tc.answer, 'selectedOption': 0} for tc in tfchoice]

    questions = []
    sidx = []
    midx = []
    tfiddx = []

    while len(sidx) != numofs:
        idx = random.randint(0, len(schoice) - 1)
        if len(sidx) < numofs and idx not in sidx:
            sidx.append(idx)
            questions.append(schoice[idx])

    while len(midx) != numofm:
        idx = random.randint(0, len(mchoice) - 1)
        if len(midx) < numofs and idx not in midx:
            midx.append(idx)
            questions.append(mchoice[idx])

    while len(tfiddx) != numoftf:
        idx = random.randint(0, len(tfchoice) - 1)
        if len(tfiddx) < numofs and idx not in tfiddx:
            tfiddx.append(idx)
            questions.append(tfchoice[idx])

    return questions


@app.route('/')
def home_page():
    return render_template("index.html")


@app.route('/index.html')
def index():
    return render_template("index.html")


@app.route('/xg.html')
def xg():
    questions = get_100_questions(5, 3, 2)
    return render_template("xg.html", questions=questions)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

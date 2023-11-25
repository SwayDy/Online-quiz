import json
import os

dir = "./2023修订版习概题库2.0"
json_file = os.listdir(dir)
json_file = [os.path.join(dir, fn) for fn in json_file]
question1 = []
for jf in json_file:
    with open(jf, "r") as f:
        question_dict = json.load(f)
        for q_d in question_dict:
            # 如果是单选题
            if q_d['qtype'] == 0:
                question1.append('xx'.join([q_d['title']] + q_d['optionList'].split('\n')[:-1] + [q_d['answer']]))

print(question1)

with open("../sChoice.txt", "w", encoding="utf-8") as f:
    for qt in question1:
        f.write(qt)
        f.write('\n')

question2 = []
for jf in json_file:
    with open(jf, "r") as f:
        question_dict = json.load(f)
        for q_d in question_dict:
            # 如果是多选题
            if q_d['qtype'] == 1:
                question2.append('xx'.join([q_d['title']] + q_d['optionList'].split('\n')[:-1] + [q_d['answer']]))

print(question2)

with open("../mChoice.txt", "w", encoding="utf-8") as f:
    for qt in question2:
        f.write(qt)
        f.write('\n')


question3 = []
for jf in json_file:
    with open(jf, "r") as f:
        question_dict = json.load(f)
        for q_d in question_dict:
            # 如果是判断题
            if q_d['qtype'] == 2:
                question3.append('xx'.join([q_d['title']] + [q_d['answer']]))

print(question3)

with open("../TFChoice.txt", "w", encoding="utf-8") as f:
    for qt in question3:
        f.write(qt)
        f.write('\n')

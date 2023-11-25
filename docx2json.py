# 读取docx中的文本代码示例
import docx
import os
import json
import random
import re


class Topic:
    def __init__(self, path, **kwargs):
        self.split_character = kwargs["Split character"]
        self.path = path
        self.question_type = kwargs["Question type"]
        self.questions = list()
        self.options = list()
        self.answers = list()
        self._init()

    def _init(self):
        paragraphs = docx.Document(self.path).paragraphs
        text = "".join([paragraph.text for paragraph in paragraphs])
        _, text = text.split(self.split_character[0])
        self.texts = []
        for sc in self.split_character[1:]:
            _text, text = text.split(sc)
            self.texts.append(_text.replace('\n', ''))
        self.texts.append(text.replace('\n', ''))
        f = lambda x: x.split('【正确答案】')
        self.texts = [f(text) for text in self.texts]
        for text in self.texts:
            while True:
                if '' in text:
                    text.pop(text.index(''))
                else:
                    break
        for n, text in enumerate(self.texts):
            answer = []
            for k, str in enumerate(text[1:]):
                if n == 1:
                    s = []
                    while True:
                        if str and 65 <= ord(str[0]) <= 68:
                            s.append(str[0])
                            str = str[1:]
                        else:
                            break
                    answer.append("".join(s))
                    text[k + 1] = str
                else:
                    answer.append(str[0])
                    text[k + 1] = str[1:]
            self.answers.append(answer)
        for text in self.texts:
            while True:
                if '' in text:
                    text.pop(text.index(''))
                else:
                    break
        for n, text in enumerate(self.texts):
            question = []
            option = []
            if n < 2:
                for str in text:
                    if not str:
                        break
                    question.append(str.split('A')[0])
                    str = ''.join([chr(k + 65) + s + '\n' for k, s in
                                   enumerate(re.split(r"[A-D]", ('A' + str.split('A')[1]))[1:])])
                    option.append(str)
                self.questions.append(question)
                self.options.append(option)
            else:
                self.questions.append(text)
                self.options.append(["是 否"] * len(text))

    def random_selection(self):
        corr = 0
        n = input("你想做几道题？")
        while int(n) <= 0:
            n = input("请不要这样？")
        for _ in range(int(n)):
            qtype = random.randint(0, 2)
            idx0 = random.randint(0, len(self.questions[qtype]) - 1)
            print(f"({self.question_type[qtype]})", end='')
            print(self.questions[qtype][idx0])
            answer = input(self.options[qtype][idx0])
            if answer == self.answers[qtype][idx0]:
                corr += 1
                print(f"答案正确")
            else:
                print(f"答案错误，正确答案为{self.answers[qtype][idx0]}")
        print(f"正确率为{corr / int(n)}")

    def json2list(self):
        topic = []
        for qtype in range(3):
            for q, o, a in zip(self.questions[qtype], self.options[qtype], self.answers[qtype]):
                tpc = {"title": q, "qtype": qtype, "optionList": o, "answer": a}
                topic.append(tpc)
        return topic


class Doex:
    def __init__(self, josn_file):
        self.name = josn_file
        self.qtype = ["单项选择题", "多项选择题", "判断题"]
        self.topic = []
        if type(self.name) == str:
            with open(self.name, "r") as f:
                self.topic = json.load(f)
        elif type(self.name) == list:
            for jf in self.name:
                with open(jf, "r") as f:
                    self.topic = self.topic + json.load(f)
        self.start()

    def __getitem__(self, item):
        return self.topic[item]

    def __len__(self):
        return len(self.topic)

    def start(self):
        print("Start do exercise!")
        while True:
            corr = 0
            n = input("你想做几道题？：")
            while int(n) <= 0:
                n = input("请输入一个大于0的整数：")
            # 生成n个随机数
            index = [random.randint(0, self.__len__() - 1) for _ in range(int(n))]
            for idx in index:
                t = self.topic[idx]
                print(f"({self.qtype[t['qtype']]})", end='')
                print(t['title'])
                myanswer = input(t['optionList'])
                if myanswer == t['answer']:
                    corr += 1
                    print("答案正确！")
                else:
                    print(f"答案错误！正确答案为{t['answer']}")
            print(f"正确率为{corr / int(n)}")
            flag = input("还想继续吗？(1:继续 0:结束)")
            if flag != '1':
                break


if __name__ == "__main__":
    print("\033[92mmade by SwayDy_水滴\ncontact lonelyswaydy@gmail.com\033[0m")
    config = {"Split character": ["一、单选题", "二、多选题", "三、判断题"],
              "Question type": ["单项选择题", "多项选择题", "判断题"]}
    for fn in os.listdir("./2023修订版习概题库"):
        topic = Topic(os.path.join("./2023修订版习概题库", fn), **config).json2list()
        with open(os.path.join("./2023修订版习概题库2.0", fn.split('.')[0] + '.json'), "w") as f:
            json.dump(topic, f)
            print(f"已写入{os.path.join('2023修订版习概题库2.0', fn.split('.')[0] + '.json')}")
    # dir = "./2023修订版习概题库2.0"
    # json_file1 = "导论.json"
    # json_file2 = "第一章世界的物质性及发展规律.json"
    # doex = Doex([os.path.join(dir, json_file1), os.path.join(dir, json_file2)])
    # config = {"Split character": ["一、单项选择题", "二、多项选择题", "三、判断题"],
    #           "Question type": ["单项选择题", "多项选择题", "判断题"]}
    # s = '\n'.join(os.listdir('./题库'))
    # while True:
    #     file_name = input(f"请输入你想要练习的章节:\n{s}\n请复制全文件名：")
    #     while file_name not in os.listdir('./题库'):
    #         file_name = input("输入有误，请重新输入：")
    #     topic = Topic(os.path.join('./题库', file_name), **config)
    #     topic.random_selection()
    #     flag = input("还想继续吗？(1:继续 0:结束)")
    #     if flag != '1':
    #         break

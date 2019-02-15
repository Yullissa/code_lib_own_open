from html.parser import HTMLParser
from urllib import request
import ssl
import pandas as pd
# 取消ssl验证
ssl._create_default_https_context = ssl._create_unverified_context
urls =[]
questions = []
class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.ques = {}
        self.last_que = None
        self.ans_flag = 0
        self.qflag = 0

    def handle_starttag(self, tag, attrs):
        # print('star: <%s> 属性 %s' % (tag ,attrs))
        def _attr(attrlist, attrname):
            for each in attrlist:
                if attrname == each[0]:
                    return each[1]
        if tag == 'div' and _attr(attrs,'data-id'):
            que  = _attr(attrs, 'data-id')
            self.last_que = que
            self.ques.update({que:[]})
        if tag == 'strong' and _attr(attrs,'class') == 'question':
            self.qflag = 1
        if tag == 'span' and _attr(attrs,'class') == "answer":
            self.ans_flag = 1


    def handle_endtag(self, tag):
        pass
        # print('end: </%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        pass
        # print('startendtag :<%s/> 结尾属性 %s' % (tag,attrs))


    def handle_data(self, data):
        # self.ques.get(self.last_que).append()
        if(self.qflag == 1):
            questions.append(data)
            self.qflag = 0
        if(self.ans_flag == 1):
            self.ques.get(self.last_que).append(data)
            self.ques.update({self.last_que : self.ques.get(self.last_que)})
            self.ans_flag = 0
        # pass

    def handle_comment(self, data):
        # print('<!--', data, '-->')
        pass

    def handle_entityref(self, name):
        # print('&%s;' % name)
        pass

    def handle_charref(self, name):
        # print('&#%s;' % name)
        pass

def movieparser(url):
    myparser = MyHTMLParser()
    with request.urlopen(url) as f:
        data = f.read().decode('utf-8')
        # print(data)
        myparser.feed(data)
        myparser.close()

    return myparser.ques


def geturl(filename):
    with open(filename) as f:
        for line in f:
            urls.append(line)

if __name__ == '__main__':
    # url = "https://rajpurkar.github.io/SQuAD-explorer/explore/1.1/dev/1973_oil_crisis.html"
    # url = 'https://movie.douban.com/'
    # 过滤掉1%的没有3个答案的结果
    geturl("inputData/crawl.txt")
    i = 0
    for url in urls:
        title = url.split('/')[-1].split('.')[0]
        ques = movieparser(url)
        qid = []
        ans1 = []
        ans2 = []
        ans3 = []
        TF_human =[]
        TF_rnet =[]
        TF_SLQA =[]
        TF_Match_LSTM=[]
        TF_LR_base =[]
        TF_Bert =[]
        qs = []
        for each in ques:
            # print(each,ques.get(each)[0])
            qid.append(each)
            qs.append(questions[i])
            i += 1
            TF_human.append('T')
            TF_rnet.append('T')
            TF_SLQA.append('T')
            TF_Match_LSTM.append('T')
            TF_LR_base.append('T')
            TF_Bert.append('T')
            if(len(ques.get(each))>=3):
                ans1.append(ques.get(each)[0])
                ans2.append(ques.get(each)[1])
                ans3.append(ques.get(each)[2])
            else:
                ans1.append("less1")
                ans2.append("less2")
                ans3.append("less3")
        df = pd.DataFrame({'question_id':qid,'questions':qs,'answer1':ans1,'answer2':ans2,'answer3':ans3,'TF_human':TF_human,'TF_rnet':TF_rnet,"TF_SLQA":TF_SLQA,"TF_Match_LSTM":TF_Match_LSTM,'TF_LR_base':TF_LR_base,'TF_Bert':TF_Bert})
        df.to_csv("{}.csv".format(title),index=False,sep=',')
        # print('%(title)s|%(rate)s|%(actors)s|%(director)s|%(duration)s' % each)
        #     pass
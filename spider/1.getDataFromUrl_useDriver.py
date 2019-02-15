from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import re
import time

options = Options()
options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
browser = webdriver.Chrome(chrome_options=options, executable_path = "D:\APP\chromedriver_win32\chromedriver.exe")

class MyHTMLParser():
    def __init__(self):
        self.wikiNameList = []
        self.paraCountlist = []
        self.data_ids = []
        self.queList = []
        self.ans1 = []
        self.ans2 = []
        self.ans3 = []
        self.TF_dict = {"human":[],"r-net": [], "SLQA": [], "Match-LSTM": [], "Logistic Regression": [], "BERT": []}
        self.modelType = self.TF_dict.keys()

    def parseTF(self,url,type):
        browser.get(url)
        time.sleep(3)
        content = browser.find_elements_by_class_name('qas-wrap')
        paraCount = 0
        # human  wikiName paraCount data-id question answer1 answer2 answer3
        # content  many qas-wrap

        for cont in content:
            for div in cont.find_elements_by_tag_name('div'):
                cla = div.get_attribute('class')
                TF_flag = 'T'
                if "wrong" in cla:
                    TF_flag = 'F'
                elif "correct" not in cla and "partial" not in cla:
                    TF_flag = 'U'
                self.TF_dict.get(type).append(TF_flag)


    def parseUrl(self,url):
        # data-id question answer1 answer2 answer3 TF-human TF-r-net TF-SLQA TF-Match-LSTM TF-Logistic Regression
        # TF-BERT
        if url.strip("\n") == "" :
            print("non url")
            return
        type = False
        for modName in self.modelType:
            if modName in url:
                print("model "+modName)
                type = True
                self.parseTF(url,modName)
                break
        if type == False:
            wikiName = url.split("/")[7].split("?")[0].split(".")[0]
            print(wikiName)
            print("human ")
            browser.get(url)
            time.sleep(3)
            content = browser.find_elements_by_class_name('qas-wrap')
            paraCount = 0
            # human  wikiName paraCount data-id question answer1 answer2 answer3
            # content  many qas-wrap
            for cont in content:
                paraCount += 1
                for i in cont.find_elements_by_tag_name('div'):
                    self.wikiNameList.append(wikiName)
                    self.paraCountlist.append(paraCount)
                    self.data_ids.append(i.get_attribute('data-id'))
                    self.queList.append(i.find_element_by_class_name('question').text)
                    answers = i.find_elements_by_class_name('answer')
                    # if len(answers) < 3:
                    #     for j in range(3 - len(answers)):
                    #         answers.append("NULL")
                    self.ans1.append(re.sub('[^A-Za-z0-9]+', '', answers[0].text))
                    self.ans2.append(re.sub('[^A-Za-z0-9]+', '', answers[1].text))
                    # self.ans3.append(answers[2].text)
                    self.TF_dict.get('human').append('T')

    def getAll(self):
        # wikiNameList = []
        # paraCountlist = []
        # data_ids = []
        # queList = []
        # ans1 = []
        # ans2 = []
        # ans3 = []
        # TF_dict = {"r-net": [], "SLQA": [], "Match-LSTM": [], "Logistic Regression": [], "BERT": []}

        df = pd.DataFrame({'wikiName':self.wikiNameList ,'paraIndex': self.paraCountlist,  'data_id': self.data_ids, 'questions':self.queList,'answer1': self.ans1, 'answer2': self.ans2,'TF_human': self.TF_dict.get('human'),'TF_rnet': self.TF_dict.get('r-net'), 'TF_SLQA':  self.TF_dict.get('SLQA'), "TF_Match_LSTM":  self.TF_dict.get('Match-LSTM'),'TF_LR_base':  self.TF_dict.get('Logistic Regression'), 'TF_Bert':self.TF_dict.get('BERT') })
        df.to_csv("new_raw_htmlresult/htmlresult.csv",index=False,sep=',')



if __name__ == '__main__':
    # url = "https://rajpurkar.github.io/SQuAD-explorer/explore/1.1/dev/1973_oil_crisis.html"
    # url = 'https://movie.douban.com/'
    # 过滤掉1%的没有3个答案的结果
    mp =  MyHTMLParser()
    mp.__init__()

    urls = []
    with open("inputData/crawled1.txt") as f:
        for line in f:
            print(line)
            mp.parseUrl(line)
    mp.getAll()
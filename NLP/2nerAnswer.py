# -*- coding: utf-8 -*-
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import nltk
import pandas as pd
import os
java_path = "C:/Program Files/Java/jdk1.8.0_181/bin/java.exe"
# java_path = "C:/../../jdk1.8.0_101/bin/java.exe"
os.environ['JAVAHOME'] = java_path

st = StanfordNERTagger('.\english.muc.7class.distsim.crf.ser.gz','.\stanford-ner.jar',encoding='utf-8')

# nltk.download('punkt')
text = 'HEllo Friday'
# print(str.isnumeric('438,000'.replace(',','')))
tokenized_text = word_tokenize(text)
classified_text = st.tag(tokenized_text)
print(classified_text)

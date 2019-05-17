#coding=utf-8

#@time:2019/4/12 16:42
#@author: Sheng Guangxiao

import jieba.analyse
import os,re
from os import path
import jieba
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud,ImageColorGenerator

d=path.dirname(__file__)

all_words=[]
ipath='LyricsSet'
lyrics=''

dictWord=dict()

count=0

for filename in os.listdir(ipath):
    with open(ipath+"\\"+filename,'rb') as f:

        content=str(f.readline().decode('utf-8'))
        result_list=re.findall('[a-zA-Z]+',content)
        for result in result_list:
            # print('result',result)
            result=str(result).lower()
            dictWord[result]=dictWord.get(result,0)+1

result=sorted(dictWord.items(),key=lambda item:item[1],reverse=True)

count=0

while count<50:
    print(result[count][0],result[count][1])
    count+=1



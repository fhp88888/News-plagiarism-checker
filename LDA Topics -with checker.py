import os
import re
import pandas as pd
import numpy as np
#Vectorize lib
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
#LDA
from sklearn.decomposition import LatentDirichletAllocation
#viewable
#import pyLDAvis
#import pyLDAvis.sklearn
#csv
import csv
#time recognize
from datetime import datetime

def getSW():
    with open("StopWords.txt", 'r',encoding="utf-8") as fp:
        stopword = fp.read()
    SWlist = stopword.splitlines()
    fp.close
    return (SWlist)

def wordCut(words):
    #cleaning
    pattern = re.compile(u'\t|\n|\.|-|:|，|。|？|：|；|……|“|”|;|\)|\(|\?|"')
    text = re.sub(pattern, '', words)
    pattern = re.compile("的| ，|和| 是| 随着| 对于| 对|等|能|都|。| |、|中|在|了|通常|如果|我们|需要|1|2|3|4|5|6|7|8|9|0")
    text = re.sub(pattern, '', text)
    #divide
    seg = pkuseg.pkuseg()
    words = seg.cut(text)
    #words is a list!
    return (" ".join (words))

def vectorize(wordslist,SWlist, n_topics):
    #I want to import "English" stop words
    #n_features = "1500"
    tf_vectorizer = CountVectorizer(strip_accents = 'unicode',
                                max_features=1500,
                                stop_words=SWlist,
                                max_df = 0.45,
                                min_df = 1)
    tf = tf_vectorizer.fit_transform(wordslist)
    #LDA topic classified
    
    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=60,learning_method='online',learning_offset=60,random_state=0, n_jobs = -1)
    lda.fit (tf)
    return (tf_vectorizer.get_feature_names(), lda, tf, tf_vectorizer)
    #return (lda.components)

      
def printTopWords(ida, feature_names, n_top_words):
    for topic_idx, topic in enumerate(ida.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i] for i in topic.argsort()[:- n_top_words - 1:-1]]))
    print ()


def lable(lda, dirlist, tf, path):
    score = lda.transform(tf)
    topicNum = len(str(score[0])) - 2
    topicNum = int(topicNum / 11)
    score = score.tolist()
    print ("I think topicNum is: ", topicNum)
    fileNo = 0
    #delete privious TopicData.csv
    try:
        os.remove("TopicData.csv")
        print("remove privious TopicData.csv")
    except:
        pass
    file = open("TopicData.csv","w",newline = "", encoding = "utf-8-sig")
    writer = csv.writer(file)
    #write body
    for each in score:
        textName = dirlist[fileNo]
        #get file size
        filePath = path + "\\" + textName
        fileSize = os.path.getsize(filePath)
        #get news No
        index1 = textName.find("._")
        textNum = int(textName[0:index1])
        #get news date
        index2 = textName.find("_", 9)
        dateRow = textName[index1 +2:index2 -2] + ":" + textName[index2 -2:index2]
        date = datetime.fromisoformat(dateRow)
        dateList = [date.year, date.month, date.day, date.hour, date.minute]
        #get news from
        index3 = textName.find("_.")
        comeFrom = textName[index2+1:index3]
        #Write
        writer.writerow([textNum, textName, textName[index3 +2:-4], fileSize] + dateList + [comeFrom] + each)
        fileNo = fileNo +1
    file.close()

def judgeLDATopic():
    #read story data file
    dataRate = []
    #start read data
    with open("TopicData.csv", encoding = "utf-8-sig") as file:
        data_row = csv.reader(file)
        for row in data_row:
            length = len(row)
            #get news topic rate
            dataRate.append([float(i) for i in row[10:length+1]])
    for baseRate in dataRate:
        #similarity select
        x = baseRate
        count = 0
        for eachFileRate in dataRate:
            if eachFileRate == baseRate:
                count +=1
        if count > 1:
            print("Test failed!")
            return("Failed")
    


def main():
    np.set_printoptions(suppress=True)
    SWlist = getSW()
    #IO
    #default
    enterdir = input ("Please enter dir: ")
    topicNum = input ("topic number start from: ")
    if enterdir == "":
        enterdir = "news story"
    targetdir = enterdir + "\\\\"
    dirlist = os.listdir(targetdir)

    df = pd.read_table("Total.txt", sep="\n",header=None)
    df.columns = ["content"]
    
    correction = 0
    while True:
        n_topics = int(topicNum) + correction
        n_top_words = 30
        (featureName,lda, tf, tf_vectorizer) = vectorize(df.content,SWlist, n_topics)
        #printTopWords(lda, featureName, n_top_words)
        #lable
        lable (lda, dirlist, tf, enterdir)
        judge = judgeLDATopic()
        if judge == "Failed":
            correction +=1
        else:
            print("Topic number check pass!")
            break
    #Data visible
    '''
    data = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
    pyLDAvis.show(data)
    '''
    print ("Program END")  
    
if __name__ == "__main__":
    main()
    

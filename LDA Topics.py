import pkuseg
import os
import re
import pandas as pd
import numpy as np
#Vectorize lib
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
#LDA
from sklearn.decomposition import LatentDirichletAllocation
#viewable
import pyLDAvis
import pyLDAvis.sklearn
#csv
import csv



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
    file = open("CSV_test.csv","w",newline = "", encoding = "utf-8-sig")
    writer = csv.writer(file)
    #write body
    for each in score:
        textTopic = each.index(max(each))
        textName = dirlist[fileNo]
        #get file size
        filePath = path + "\\" + textName
        fileSize = os.path.getsize(filePath)
        #get file No
        index = textName.find("._")
        if index != -1:
            try:
                textNum = int(textName[0:index])
            except:
                print("Numbering Err: ", textName," ignored.")
                break
        #Write
        writer.writerow([textName, textTopic, fileSize, textNum] + each)
        fileNo = fileNo +1
    file.close()

def main():
    np.set_printoptions(suppress=True)
    SWlist = getSW()
    #IO
    #default
    
    #When total.txt exist
    enterdir = input ("Please enter dir: ")
    #enterdir = "C:\\Users\\HiFan\\Desktop\\新建文件夹\\ATK\\there"
    targetdir = enterdir + "\\\\"
    dirlist = os.listdir(targetdir)
    
    #up

    df = pd.read_table("Total.txt", sep="\n",header=None)
    df.columns = ["content"]
    
    n_topics = 90
    n_top_words = 30
    (featureName,lda, tf, tf_vectorizer) = vectorize(df.content,SWlist, n_topics)

    printTopWords(lda, featureName, n_top_words)
    print (df.shape)
    #lable
    
    lable (lda, dirlist, tf, enterdir)

    #Data visible

    data = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
    pyLDAvis.show(data)
    
    print ("Program END")  
    
if __name__ == "__main__":
    main()
    

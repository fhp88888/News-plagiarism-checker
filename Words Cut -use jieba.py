import jieba
import os
import re
import pandas as pd
import numpy as np

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
    words = jieba.lcut(text)
    #words is a list!
    return (" ".join (words))

def main():
    np.set_printoptions(suppress=True)
    SWlist = getSW()
    #IO
    #default
    enterdir = input ("Please enter your dir: ")
    if enterdir == "":
        enterdir = "news story\\"
    enterdir = enterdir.replace ("\\", "\\\\")
    targetdir = enterdir + "\\\\"
    dirlist = os.listdir(targetdir)
    count = 0
    totalLen = len(dirlist)
    for eachfile in dirlist:
        fileAddress = targetdir + eachfile
        with open(fileAddress, "r", encoding="utf-8") as fd:
            fileData = fd.read()
        #clean data
        fileData = fileData.replace ("\n"," ")
        #cut data
        fileData = wordCut(fileData)
        #clean data end
        newfiledir = targetdir + "Total.txt"
        with open ("Total.txt", "a", encoding="utf-8") as fd:
            fd.write(fileData)
            fd.write ("\n")
        count +=1
        if count % 1000 ==0:
            print("Processing:", 100 * count/totalLen,"%")
    print ("Program END")  
    
if __name__ == "__main__":
    main()
    

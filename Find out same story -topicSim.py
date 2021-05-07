import csv
import os
import numpy as np
  
def cosSimilarityCaculate(newsIndex, dataRate, newsTopicName):
    sameFileIndexList = []
    for baseRate in dataRate:
        #similarity select
        x = baseRate
        otherSim = []
        for eachFileRate in dataRate:
            y = eachFileRate
            res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
            cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))
            if cos >=0.9999999999:
                #don't count the same file
                if dataRate.index(baseRate) != dataRate.index(eachFileRate):
                    #sim file decteced
                    otherSim.append(newsIndex[dataRate.index(eachFileRate)])
        '''
        if len(otherSim) != 0:
            print(newsTopicName[dataRate.index(baseRate)])
            print(newsIndex[dataRate.index(baseRate)])
            for each in otherSim:
                print(newsTopicName[newsIndex.index(each)])
                print(each)
            print("-"*20)
        '''
        sameFileIndexList.append(otherSim)
    return(sameFileIndexList)

def main():
    #read story data file
    newsIndex = []
    dataRate = []
    newsWords = []
    newsDate = []
    newsPublisher = []
    newsTopicName = []
    #start read data
    with open("TopicData.csv", encoding = "utf-8-sig") as file:
        data_row = csv.reader(file)
        for row in data_row:
            length = len(row)
            #get news index
            newsIndex.append(int(row[0]))
            #get news topic name
            newsTopicName.append(row[1])
            #get news size
            newsWords.append(int(row[2]))
            #get news published date
            newsDate.append([int(row[i]) for i in range(3,8)])
            #get news publisher
            newsPublisher = row[8]
            #get news topic rate
            dataRate.append([float(i) for i in row[9:length+1]])
    print("Read ", len(newsIndex), " from CSV.")
    
    #find same file
    cosResult = cosSimilarityCaculate(newsIndex, dataRate, newsTopicName)
    #personNameResult = personNameSimilarity()
    #locationSimResult = locationSimilarity()

    #give result
    #copyResult = copyJudge()

    #save result to file
    #saveResult()

if __name__  == "__main__":
    main()
    print("Complated !")

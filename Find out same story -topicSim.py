import csv
import os
import numpy as np
import pkuseg

def pkusegWordsCut(content):
    seg = pkuseg.pkuseg(postag=True)  #show words tag
    result = seg.cut(content)
    return(result)
    #return sample
    #[('我', 'r'), ('是', 'v'), ('小明', 'nr'), ('，', 'w'), ('我', 'r'), ('爱', 'v'), ('北京', 'ns'), ('天安门', 'ns')]

def personNameChecker(eachJudge, fileContent):
    personNameCheckResult = []
    nameList = []
    #for each passage
    for eachPassage in fileContent:
        passageNameList = []
        #for each words in each passage
        for eachWords in eachPassage:
            if eachWords[1] == "nr":
                #don't add same person name that record before
                if eachWords[0] not in passageNameList:
                    #print("find a person name")
                    passageNameList.append(eachWords[0])
        if len(passageNameList) == 0:
            print("Not find person name in this passages")
            passageNameList.append("None")
        nameList.append(passageNameList)
    #check if there is same person name
    sameNameFileResult = []
    #check if the base file has no person name
    if nameList[0][0] != "None":
        checkName = nameList[0]
        #the first passage has at least one person name
        for eachPassage in nameList[1:]:
            for each in eachPassage:
                if each in checkName:
                    print("Same name has been finded")
                    #add same file index to sameNameFileResult list
                    sameNameFileResult.append(eachJudge[nameList.index(eachPassage)])
                    break
        if len(sameNameFileResult) == 0:
            #this means there is no same person name in this file
            print("no same person name")
        else:
            #this means there is at least one same person name
            #add base file to same list
            sameNameFileResult.append(eachJudge[0])
            personNameCheckResult = sameNameFileResult
    else:
        #the base file has no person name, we cannot identify same file
        print("the base file has no person name")
        personNameCheckResult = eachJudge
        
    return(personNameCheckResult)

def locationNameChecker(eachJudge, fileContent):
    LocationNameCheckResult = []
    nameList = []
    #for each passage
    for eachPassage in fileContent:
        passageNameList = []
        #for each words in each passage
        for eachWords in eachPassage:
            if eachWords[1] == "ns":
                #don't add same Location name that record before
                if eachWords[0] not in passageNameList:
                    #print("find a Location name")
                    passageNameList.append(eachWords[0])
        if len(passageNameList) == 0:
            print("Not find Location name in this passages")
            passageNameList.append("None")
        nameList.append(passageNameList)
    #check if there is same Location name
    sameNameFileResult = []
    #check if the base file has no Location name
    if nameList[0][0] != "None":
        checkName = nameList[0]
        #the first passage has at least one Location name
        for eachPassage in nameList[1:]:
            for each in eachPassage:
                if each in checkName:
                    print("Same location name has been finded")
                    #add same file index to sameNameFileResult list
                    sameNameFileResult.append(eachJudge[nameList.index(eachPassage)])
                    break
        if len(sameNameFileResult) == 0:
            #this means there is no same Location name in this file
            print("no same location name")
        else:
            #this means there is at least one same Location name
            #add base file to same list
            sameNameFileResult.append(eachJudge[0])
            LocationNameCheckResult = sameNameFileResult
    else:
        #the base file has no Location name, we cannot identify same file
        print("the base file has no Location name")
        LocationNameCheckResult = eachJudge

    return(LocationNameCheckResult)

def sameWordsProcess(cosResult, newsIndex, newsTopicName, newsFileName):
    for eachJudge in cosResult:
        #read data
        fileContent = []
        for eachStory in eachJudge:
            #get story direction
            storyDir = "A:\\news identification project\\news story\\" + newsFileName[newsIndex.index(eachStory)]
            print(storyDir)
            with open(storyDir, "r", encoding = "utf-8") as file:
                storyContent = file.read().replace("\n", " ")
            wordsTag = pkusegWordsCut(storyContent)
            fileContent.append(wordsTag)
        print("successfully read data")
        #Person Name check
        personNameCheckResult = personNameChecker(eachJudge, fileContent)
        print(personNameCheckResult)
        #Location Name check
        locationNameCheckResult = locationNameChecker(eachJudge, fileContent)
        print(locationNameCheckResult)

def cosSimilarityCaculate(newsIndex, dataRate, newsTopicName):
    sameFileIndexList = []
    for baseRate in dataRate:
        #similarity select
        x = baseRate
        otherSim = [] + [newsIndex[dataRate.index(baseRate)]]
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
        #if we have same file, then append it to list
        if len(otherSim) > 1:
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
    newsFileName = []
    #start read data
    with open("TopicData.csv", encoding = "utf-8-sig") as file:
        data_row = csv.reader(file)
        for row in data_row:
            length = len(row)
            #get news index
            newsIndex.append(int(row[0]))
            #get news topic name
            newsTopicName.append(row[2])
            #get news size
            newsWords.append(int(row[3]))
            #get news published date
            newsDate.append([int(row[i]) for i in range(4,9)])
            #get news publisher
            newsPublisher = row[9]
            #get news topic rate
            dataRate.append([float(i) for i in row[10:length+1]])
            #get news story full name
            newsFileName.append(row[1])
    print("Read ", len(newsIndex), " from CSV.")
    #LDA same topic accquire
    cosResult = cosSimilarityCaculate(newsIndex, dataRate, newsTopicName)
    print(cosResult)
    #same words accquire
    sameWordsResult = sameWordsProcess(cosResult, newsIndex, newsTopicName, newsFileName)
    #locationSimResult = locationSimilarity()

    #give result
    #copyResult = copyJudge()

    #save result to file
    #saveResult()

def test():
    print("test start!")
    #read story data file
    newsIndex = []
    dataRate = []
    newsWords = []
    newsDate = []
    newsPublisher = []
    newsTopicName = []
    newsFileName = []
    #start read data
    with open("TopicData.csv", encoding = "utf-8-sig") as file:
        data_row = csv.reader(file)
        for row in data_row:
            length = len(row)
            #get news index
            newsIndex.append(int(row[0]))
            #get news topic name
            newsTopicName.append(row[2])
            #get news size
            newsWords.append(int(row[3]))
            #get news published date
            newsDate.append([int(row[i]) for i in range(4,9)])
            #get news publisher
            newsPublisher = row[9]
            #get news topic rate
            dataRate.append([float(i) for i in row[10:length+1]])
            #get news story full name
            newsFileName.append(row[1])
    print("Read ", len(newsIndex), " from CSV.")
    
    cosResult = [[158, 414], [24, 70]]
    sameWordsProcess(cosResult, newsIndex, newsTopicName, newsFileName)
    
if __name__  == "__main__":
    test()
    print("Complated !")

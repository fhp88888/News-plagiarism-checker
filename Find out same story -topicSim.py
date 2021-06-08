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
            print("Hasn't find person name in this passages")
            passageNameList.append("None")
        nameList.append(passageNameList)
    #check if there is same person name
    sameNameFileResult = []
    #check if the base file has no person name
    if nameList[0][0] != "None":
        checkName = nameList[0]
        #the first passage has at least one person name
        
        for thisNameList in range(1,len(nameList)):
            eachPassage = nameList[thisNameList]
            count = 0
            for each in eachPassage:
                if each in checkName:
                    #print("Same name has been finded")
                    count +=1
            #Consider only files contain more than 70% same name as same file
            if count > int(0.7 * len(checkName)):
                #add same file index to sameNameFileResult list
                sameNameFileResult.append(eachJudge[thisNameList])
                
        if len(sameNameFileResult) == 0:
            #this means there is no same person name in this file
            print("no same person name")
        else:
            #this means there is at least one same person name
            #add base file to same list
            sameNameFileResult = [eachJudge[0]] + sameNameFileResult
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
            print("Hasn't find Location name in this passages")
            passageNameList.append("None")
        nameList.append(passageNameList)
    #check if there is same Location name
    sameNameFileResult = []
    #check if the base file has no Location name
    if nameList[0][0] != "None":
        checkName = nameList[0]
        #the first passage has at least one Location name

        for thisNameList in range(1,len(nameList)):
            eachPassage = nameList[thisNameList]
            count = 0
            for each in eachPassage:
                if each in checkName:
                    #print("Same name has been finded")
                    count +=1
            #Consider only files contain more than 70% same name as same file
            if count > int(0.7 * len(checkName)):
                #add same file index to sameNameFileResult list
                sameNameFileResult.append(eachJudge[thisNameList])
                
        if len(sameNameFileResult) == 0:
            #this means there is no same Location name in this file
            print("no same location name")
        else:
            #this means there is at least one same Location name
            #add base file to same list
            sameNameFileResult = [eachJudge[0]] + sameNameFileResult
            LocationNameCheckResult = sameNameFileResult
    else:
        #the base file has no Location name, we cannot identify same file
        print("the base file has no Location name")
        LocationNameCheckResult = eachJudge

    return(LocationNameCheckResult)

def sameWordsProcess(cosResult, newsIndex, newsTopicName, newsFileName):
    sameWordsProcessList = []
    priviousFileContent = []
    priviousFileContentIndex = []
    for eachJudge in cosResult:
        #read data
        fileContent = []
        for eachStory in eachJudge:
            #check if we have process this file before
            if eachStory in priviousFileContentIndex:
                #we have process this file before
                print("load data")
                fileContent.append(priviousFileContent[priviousFileContentIndex.index(eachStory)])
            else:
                #we have not process this file before
                #get story direction
                storyDir = "A:\\news identification project\\news story\\" + newsFileName[newsIndex.index(eachStory)]
                print(storyDir)
                with open(storyDir, "r", encoding = "utf-8") as file:
                    storyContent = file.read().replace("\n", " ")
                wordsTag = pkusegWordsCut(storyContent)
                fileContent.append(wordsTag)
                #save this data for further use
                priviousFileContent.append(wordsTag)
                priviousFileContentIndex.append(eachStory)
        print("successfully read data")
        #Person Name check
        personNameCheckResult = personNameChecker(eachJudge, fileContent)
        print("Person name check result:", personNameCheckResult)
        #Location Name check
        locationNameCheckResult = locationNameChecker(eachJudge, fileContent)
        print("Location name check result:", locationNameCheckResult)
        #cross check
        #check if two list is empty
        crossCheckFile = []
        if len(personNameCheckResult) > 0 and len(locationNameCheckResult) > 0:
            for each in personNameCheckResult:
                if each in locationNameCheckResult:
                    #this is same file
                    crossCheckFile.append(each)
        print("Cross check file: ", crossCheckFile)
        if len(crossCheckFile) > 1:
            sameWordsProcessList.append(crossCheckFile)

    return(sameWordsProcessList)

def cosSimilarityCaculate(newsIndex, dataRate, newsTopicName):
    sameFileIndexList = []
    eachFileRate02 = 0 #debug
    for baseRateIndex in range(0, len(dataRate)):
        baseRate = dataRate[baseRateIndex]
        #similarity select
        x = baseRate
        otherSim = [newsIndex[baseRateIndex]]
        for eachFileRateIndex in range(0, len(dataRate)):
            eachFileRate = dataRate[eachFileRateIndex]
            y = eachFileRate
            res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
            cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))
            if cos >=0.9999999999:
                '''
                #debug block
                if newsIndex[baseRateIndex] == 326:
                    print("326 is here")
                    print("eachFileRateIndex: ", eachFileRateIndex)
                    print("newsIndex: ", newsIndex[eachFileRateIndex])
                '''
                #don't count the base file
                if baseRateIndex != eachFileRateIndex:
                    #sim file decteced
                    otherSim.append(newsIndex[eachFileRateIndex])
                    
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
    print(sameWordsResult)

    #save result to file
    #saveResult()

def test():
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
    cosResult = cosSimilarityCaculate(newsIndex, dataRate, newsTopicName)
    print(cosResult)
    #cosResult = [[340, 329, 372]]
    #same words accquire
    sameWordsResult = sameWordsProcess(cosResult, newsIndex, newsTopicName, newsFileName)
    print(sameWordsResult)

    #save result to file
    #saveResult()
    
if __name__  == "__main__":
    test()
    print("Complated !")

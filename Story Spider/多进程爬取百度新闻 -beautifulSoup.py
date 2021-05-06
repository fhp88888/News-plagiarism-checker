import requests
from bs4 import BeautifulSoup
import re
import time
import os
import threading
import winsound
threadingCount = 0

class IO(object):
    def add(Title, Date, ComeFrom, Content):
        #remove not allow words
        Title = IO.removeNotAlllowedWords(Title)
        Date = IO.removeNotAlllowedWords(Date)
        ComeFrom = IO.removeNotAlllowedWords(ComeFrom)
        #add file
        FileName = "A:\\news identification project\\news story\\" + Date+ "_" + ComeFrom + "_." + Title + ".txt"
        #try to delete privious file
        try:
            os.remove(FileName)
            print("Same file deceted, deleting formal file")
        except:
            pass
        file_handle = open (FileName, mode = "a", encoding='utf-8')
        file_handle.write(Title)
        file_handle.write('\n')
        try:
            file_handle.write(Content)
        except:
            print ("ERR!!!!!")
            print (Title)
            print (Content)
        file_handle.write('\n')
        file_handle.close()
    def removeNotAlllowedWords(raw):
        notAllow = [":","/","\\","*","?","？","|"]
        for each in notAllow:
            raw = raw.replace(each, "")
        return raw
    def log(title):
        winsound.Beep(600,100)
        file_handle = open ("errLog.txt", mode = "a", encoding='utf-8')
        file_handle.write(title)
        file_handle.write('\n')
        file_handle.close()
        
class GetText(object):
    def __init__(self, url):
        self.url = url
        self.SourceCode = self.getit()
        self.soup = BeautifulSoup(self.SourceCode, "lxml")
    def getit(self):
        #proxy = {"http":"127.0.0.1:10809", "https":"127.0.0.1:10809"}
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
        req = requests.get(self.url, headers = headers)
        if req.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(req.text)
            if encodings:
                encoding = encodings[0]
            else:
                encoding = req.apparent_encoding
            # encode_content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
            global encode_content
            encode_content = req.content.decode(encoding, 'replace') #如果设置为replace，则会用?取代非法字符；
            #print (encode_content)
            return(encode_content)
        return(req.text)
    def Content(self):
        content = self.soup.find_all("p")
        words = ""
        for i in range(0,len(content)):
            words += content[i].text
        return(words)
    def getTitle(self):
        return self.soup.find_all("h2")[0].text        
    def getDate(self):
        date = self.soup.find_all("div", class_ = "index-module_articleSource_2dw16")[0]
        for eachSpan in date.find_all("span"):
            index = str(eachSpan).find("发布时间:")
            if index != -1:
                d1 = str(eachSpan)[index+6:index+11].replace("-","月") + "日"
        d2 = date.find_all("span", class_ = "index-module_time_10s4U")[0].text
        return("2021年"+d1+" "+str(d2).replace(":",""))
    def getComeFrom(self):
        return self.soup.find_all("p", class_="index-module_authorName_7y5nA")[0].text
    def getNewsList(self):
        urlList = []
        lista = self.soup.find_all("a")
        for eacha in lista:
            try:
                #don't download video news
                if eacha.find_all("span", class_ = "related-video-icon") == []:
                    href = str(eacha["href"])
                    if href.find("baijiahao") != -1:
                        urlList.append(href)
            except:
                pass
        return(urlList)

def getNewsList():
    FromList = ["http://news.baidu.com/", "http://news.baidu.com/guonei/", "http://news.baidu.com/guoji/", "http://news.baidu.com/finance/",
                "http://news.baidu.com/ent/", "http://news.baidu.com/sports/", "http://news.baidu.com/internet/", "http://news.baidu.com/tech/", "http://news.baidu.com/game/"]
    Thread = [GetText(url) for url in FromList]
    urlList = []
    for each in Thread:
        urlList += each.getNewsList()
    return(urlList)

def download_test(url):
    Page = GetText(url)
    Content = Page.Content()
    Title = Page.getTitle()
    Date = Page.getDate()
    ComeFrom = Page.getComeFrom()
    print(Title, Date, ComeFrom)
    #IO.add(Title, Date, ComeFrom, Content)
    print("Download one")

class download(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
    def run(self):
        global threadingCount
        try:
            Page = GetText(self.url)
            Content = Page.Content()
            Title = Page.getTitle()
            Date = Page.getDate()
            ComeFrom = Page.getComeFrom()
            IO.add(Title, Date, ComeFrom, Content)
        except:
            print("Err:", self.url)
            IO.log(self.url)
        print("Download one")
        threadingCount -= 1

def atc():
    global threadingCount
    print("Start Downloading")
    urlList = getNewsList()
    print("This time we have total", len(urlList), "news.")
    multiTask = [download(url) for url in urlList]
    for eachTask in multiTask:
        #alive threads amount control
        while threadingCount > 5:
            time.sleep(0.2)
        eachTask.start()
        threadingCount += 1
        print ("Starting new thread. Now alive:", threadingCount)
        time.sleep(0.2)
    for eachTask in multiTask:
        eachTask.join()
    print("All download complated")
        
if __name__ == "__main__":
    atc()

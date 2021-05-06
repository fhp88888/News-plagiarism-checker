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
        req = requests.get(self.url )
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
    def Content(self):
        content = self.soup.select('.article p')
        words = ""
        for i in range(0,len(content)):
            words += content[i].text
        return(words)
    def getTitle(self):
        return self.soup.find_all("h1", class_ = "main-title")[0].text        
    def getDate(self):
        dateRow = str(self.soup.find_all("span", class_ = "date")[0].text)
        #standardlize
        date = dateRow.replace("年", "-").replace("月", "-").replace("日", "")
        return date
    def getComeFrom(self):
        return self.soup.find_all(class_="source")[0].text
    def getNewsList(self):
        ListRow = re.findall("https://news.sina.com.cn/c/(.*?).shtml", self.SourceCode)
        List = []
        for each in ListRow:
            List.append("https://news.sina.com.cn/c/" + each + ".shtml")
        return(List)

def getNewsList():
    worldNews = GetText("https://news.sina.com.cn/world/")
    chinaNews = GetText("https://news.sina.com.cn/china/")
    return(worldNews.getNewsList() + chinaNews.getNewsList())

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
        while threadingCount > 10:
            time.sleep(0.1)
        eachTask.start()
        threadingCount += 1
        print ("Starting new thread. Now alive:", threadingCount)
        time.sleep(0.1)
    for eachTask in multiTask:
        eachTask.join()
    print("All download complated")
        
if __name__ == "__main__":
    atc()

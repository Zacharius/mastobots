#!/usr/bin/python3

import feedparser
#feedparser docs: https://pythonhosted.org/feedparser/

LATEST_TITLE_DIR= "/home/z/prj/mastobots/rssTitles/"

class Parser:

    def __init__(self, feedURLList):
        self.feedURLList = feedURLList
        
    def getNewPosts(self):

        newEntries = []
        
        for feedURL in self.feedURLList:
            feed = feedparser.parse(feedURL)
            latestTitleFile = generateFileName(feed)

            try:
                latestTitle = findLatestTitle(latestTitleFile)
            except:
                latestTitle = ""

            newestTitle = feed.entries[0].title

            for entry in feed.entries:
                if latestTitle == entry.title:
                    break
                newEntries.append(entry)


            writeLatestTitle(latestTitleFile, newestTitle)

        return newEntries



#check file for latest title accessed
def findLatestTitle(fileName):
    with open(fileName) as file:
        title = file.read()

    return title

#write latest title to file
def writeLatestTitle(fileName, title):
    with open(fileName, "w") as file:
        file.write(title)

def generateFileName(feed):
    base = feed.feed.title
    base = base.replace(" ","_")
    fileName = LATEST_TITLE_DIR + base + '.txt'

    return fileName

if __name__ == '__main__':
    feedURLList = [ "https://www.ribbonfarm.com/feed/" ]
    parser = Parser(feedURLList)
    entries = parser.getNewPosts()

    for entry in entries:
        print(entry.title)
    

    

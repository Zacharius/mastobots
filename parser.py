#!/usr/bin/python3

import feedparser
import os
from util import getAbsolutePath
#feedparser docs: https://pythonhosted.org/feedparser/

LATEST_TITLE_DIR= getAbsolutePath(__file__, 'rssTitles/')

class Parser:

    def __init__(self, feedURLList):
        self.feedURLList = feedURLList
        
    def getNewPosts(self):

        newEntries = []
        
        for feedURL in self.feedURLList:
            feed = feedparser.parse(feedURL)
            latestTitleFile = generateFileName(feedURL)
            if len(feed.entries) > 0:
                newestTitle = feed.entries[0].title
            else:
                continue

            try:
                latestTitle = findLatestTitle(latestTitleFile)
            except:
                latestTitle = newestTitle


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

def generateFileName(url):
    base = ''.join(e for e in url if e.isalnum())
    #base = feed.feed.title
    #base = base.replace(" ","_")
    fileName = LATEST_TITLE_DIR + base + '.txt'

    return fileName

if __name__ == '__main__':
    feedURLList = [ "https://www.ribbonfarm.com/feed/" ]
    parser = Parser(feedURLList)
    entries = parser.getNewPosts()

    for entry in entries:
        print(entry.title)
    

    

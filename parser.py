#!/usr/bin/python3

import feedparser
#feedparser docs: https://pythonhosted.org/feedparser/

feedURL = "https://stallman.org/rss/rss.xml"
latestTitleFile = "lastTitle.txt"

def getNewPosts():



    feed = feedparser.parse(feedURL)
    try:
        latestTitle = findLatestTitle(latestTitleFile)
    except:
        latestTitle = ""

    newestTitle = feed.entries[0].title
    newEntries = []
    
    for entry in feed.entries:
        if latestTitle == entry.title:
            break
        newEntries.append(entry)
        

    writeLatestFile(latestTitleFile, newestTitle)

    return newEntries




#check file for latest title accessed
def findLatestTitle(fileName):
    with open(fileName) as file:
        title = file.read()

    return title

#write latest title to file
def writeLatestFile(fileName, title):
    with open(fileName, "w") as file:
        file.write(title)

if __name__ == '__main__':
    getNewPosts()


    

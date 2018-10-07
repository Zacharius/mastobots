#!/usr/bin/python3


import os
import subprocess
from datetime import date, timedelta
from util import getAbsolutePath
from format import formatBlogLog, formatLinkedTootLog, formatLocalTootLog, extractExternalLinks

def main():
    logDir = getAbsolutePath(__file__, 'log/')
    logfile = "out.txt"
    logger = Logger(logDir, logfile)


    logger.archive()
    logger.logBlog('who', 'what', 'why')

class Logger:
    blogPostsSection = '* New Posts'
    readSection = '* Stuff We Read'
    opinionSection = '* Short Takes'

    def __init__(self, logDir, logFile):
        self.logfile = str(logDir +  logFile)

        
    def logBlog(self, title, author, link):
        logBlogString = formatBlogLog(title, author, link)
        self.__insertAfterString(self.blogPostsSection, logBlogString)
    
                      

    def logToot(self, text, author):
        externalLinks = extractExternalLinks(text)
        if not externalLinks:
            self.__logLocalToot(text, author)
        else:
            self.__logLinkedToot(text, author)

    def __logLinkedToot(self, text, author):
        linkedTootString = formatLinkedTootLog(text, author)
        self.__insertAfterString(self.readSection, logBlogString)

    def __logLocalToot(self, text, author):
        localTootString = formatLocalTootLog(text, author)
        self.__insertAfterString(self.opinionSection, logBlogString)

    # WARNING: this function places all of self.logfile into memory,
    #          could cause problems if file gets to big, which I don't
    #          anticipate
    def __insertAfterString(self, seekString, insertString):
        with open(self.logfile, 'r') as log:
           logText = log.read()

        logText = logText.replace(seekString, seekString + '\n' + insertString, 1)

        with open(self.logfile, 'w') as log:
            log.write(logText)
            
    def archive(self):
        datepostfix = date.today().strftime("%y.%W")

        archiveFile = self.logfile + "." + datepostfix

        subprocess.run(['mv', self.logfile, archiveFile])

        self.__prepNewLogfile()

       
    
    def __prepNewLogfile(self):
        startDate = date.today()
        startDateString = startDate.strftime('%m/%d/%y')
        endDate = startDate + timedelta(days=6)
        endDateString = endDate.strftime('%m/%d/%y')

        with open(self.logfile, 'a') as log:
            log.write('Refactorings Roundup ' +
                      startDateString +
                      ' -- ' +
                      endDateString + '\n')
            log.write(self.blogPostsSection + '\n')
            log.write(self.readSection + '\n')
            log.write(self.opinionSection + '\n')

    
        


if __name__ == "__main__":
    main()
        
    

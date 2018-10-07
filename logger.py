#!/usr/bin/python3


import os
import re
import time
import subprocess
from datetime import date, timedelta
from util import getAbsolutePath
from format import formatBlogLog, formatLinkedTootLog, formatLocalTootLog, extractExternalLinks

def main():
    logDir = getAbsolutePath(__file__, 'log/')
    logfile = "out.txt"
    logger = Logger(logDir, logfile)


    logger.archive()

class Logger:

    def __init__(self, logDir, logFile):
        self.logfile = str(logDir +  logFile)

        
    def logBlog(self, title, author, link):
        logBlogString = formatBlogLog(title, author, link)
        with open(self.logfile, "a") as log:
            log.write(logBlogString)
                      

    def logToot(self, text, author):
        externalLinks = extractExternalLinks(text)
        if not externalLinks:
            self.__logLocalToot(text, author)
        else:
            self.__logLinkedToot(text, author)

    def __logLinkedToot(self, text, author):
        linkedTootString = formatLinkedTootLog(text, author)
        with open(self.logfile, "a") as log:
            log.write(linkedTootString)
                      
    def __logLocalToot(self, text, author):
        localTootString = formatLocalTootLog(text, author)
        with open(self.logfile, 'a') as log:
            log.write(localTootString)

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
            log.write("* New Posts\n")
            log.write('* Stuff We Read\n')
            log.write('* Short Takes\n')
        


if __name__ == "__main__":
    main()
        
    

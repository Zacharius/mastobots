#!/usr/bin/python3


import os
import re
import time
import subprocess
import datetime
from util import getAbsolutePath
from format import formatBlogLog, formatLinkedTootLog, formatLocalTootLog

def main():
    logDir = getAbsolutePath(__file__, 'log/')
    logfile = "out.txt"
    logger = Logger(logDir, logfile)

    text = ''' <p>Design thinking is inherently conservative <a
    href="https://refactorcamp.org/tags/heyfeedfox" class="mention hashtag" rel="tag">#<span>heyfeedfox</span></a> <a
    href="https://hbr.org/2018/09/design-thinking-is-fundamentally-conservative-and-preserves-the-status-quo"
    rel="nofollow noopener" target="_blank"><span
    class="invisible">https://</span><span
    class="ellipsis">hbr.org/2018/09/design-thinkin</span><span
    class="invisible">g-is-fundamentally-conservative-and-preserves-the-status-quo</span></a></p>
    vgr '''
    title = "poetry"
    link = "zfadd.is"
    author = "@zacharius"

    logger.logToot(text, author)

class Logger:

    def __init__(self, logDir, logFile):
        self.logfile = str(logDir +  logFile)

        
    def logBlog(self, title, author, link):
        logBlogString = formatBlogLog(title, author, link)
        with open(self.logfile, "a") as log:
            log.write(logBlogString)
            log.write()#newline
                      

    def logToot(self, text, author):
        externalLinks = extractExternalLinks(text)
        if not externalLinks:
            self.__logLocalToot(text, author)
        else:
            self.__logLinkedToot(text, author, externalLinks)

    def __logLinkedToot(self, text, author):
        linkedTootString = formatLinkedTootLog(text, author)
        with open(self.logfile, "a") as log:
            log.write(linkedTootString)
                      
    def __logLocalToot(self, text, author):
        localTootString = formatLocalTootLog(text, author)
        with open(self.logfile, 'a') as log:
            log.write(localTootString)

    def archive(self):
        datepostfix = datetime.date.today().strftime("%y.%W")

        archiveFile = self.logfile + "." + datepostfix

        subprocess.run(['mv', self.logfile, archiveFile])
                       
        


if __name__ == "__main__":
    main()
        
    

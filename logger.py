#!/usr/bin/python3


import os
import re
import time
import subprocess
import datetime

def main():
    logDir = "/home/zacharius/Project/Mastobots/log/"
    logfile = "out.txt"
    logger = Logger(logDir, logfile)

    text = "One Potato is not enough to make a stew"
    title = "poetry"
    link = "zfadd.is"
    author = "@zacharius"

    logger.log(text, title, author, link)
    logger.log(text, title, author, link)

    logger.archive()

class Logger:

    def __init__(self, logDir, logFile):
        self.logfile = str(logDir +  logFile)

        
    def logBlog(self, text, title, author, link):

        with open(self.logfile, "a") as log:

            log.write('<a href="' + link + '">' + title + '</a> ')
            log.write('by ' + author + '\n\n')
        

            log.write(text + "\n")
            log.write("--------------------\n")


    def logToot(self, text, author):

        with open(self.logfile, "a") as log:

            log.write(text + "\n")
            log.write(author + "\n")
            log.write("---------------------\n")

            
    def archive(self):
        datepostfix = datetime.date.today().strftime("%y.%W")

        archiveFile = self.logfile + "." + datepostfix

        subprocess.run(['mv', self.logfile, archiveFile])
                       
        


if __name__ == "__main__":
    main()
        

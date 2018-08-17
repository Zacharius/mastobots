#!/usr/bin/python3

from logger import Logger


logDir = '/home/z/prj/mastobots/log/'
logfile = 'out.txt'
logger = Logger(logDir, logfile)

logger.archive()

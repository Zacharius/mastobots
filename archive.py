#!/usr/bin/python3

from logger import Logger
from util import getAbsolutePath

logDir = getAbsolutePath(__file__, 'log/')
logfile = 'out.txt'
logger = Logger(logDir, logfile)

logger.archive()

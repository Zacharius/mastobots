#!/usr/bin/python3

from mastodon import Mastodon
#mastodon docs: https://mastodonpy.readthedocs.io/en/latest/
from parser import getNewPosts
import os
import re

def main():

    stallminator = login()
    rssEntries = getNewPosts()

    if len(rssEntries) > 5:
        rssEntries = rssEntries[:5]

    for entry in rssEntries:
        status = formatStatus(entry)
        print(entry.title)
        print(status)
        print('----------------------')
        stallminator.status_post(
            status,
            spoiler_text=entry.title,
            visibility="private")
    
def formatStatus(rssEntry):
    status = rssEntry.description
    status = removeInternalNewlines(status)
    status = htmlToMastodonFormat(status)
    status = concatAndInsertLink(status, rssEntry)
    return status
    
def concatAndInsertLink(status, rssEntry):
    maxStatusLen = 500
    statusLen = len(status)
    headerLen = len(rssEntry.title)
    #mastodon only counts the first 30 chars of a link towards its status limit,
    #the other 2 are for newlines before the link
    totalLen = statusLen+headerLen+32

    if totalLen <= maxStatusLen:
        status += '\n\n'
    else:
        shortenedStatusLen = statusLen - (totalLen - maxStatusLen) - 3
        status = status[: shortenedStatusLen]
        status += '...\n\n'

    status += rssEntry.link
    return status
        
def removeInternalNewlines(status):
    status = status.replace("\n", " ")
    return status

def htmlToMastodonFormat(status):
    status = replacePtags(status)
    status = replaceLItags(status)
    status = replaceAtags(status)
    return status

def replaceLItags(status):
    status = status.replace("<li>", "")
    status = status.replace("</li>", "\n")
    return status

# replace p tags with new line
def replacePtags(status):
    status = status.replace("<p>", "")
    status = status.replace("</p>", "\n")
    return status
    
def replaceAtags(status):
    status = re.sub(r'<a href="(.*?)">(.*?)<\/a>', r'\2, \1 ', status)
    return status

def login():
    access = Mastodon(
        client_id = "/home/z/prj/Stallminator/stallminator_clientcred.secret")

    access.log_in(
        'zach.faddis@gmail.com',
        os.environ['STALLMINATOR_PASSWORD'],
        to_file = '/home/z/prj/Stallminator/stallminator_usercred.secret')

    stallminator = Mastodon(
        access_token = '/home/z/prj/Stallminator/stallminator_usercred.secret')

    return stallminator

if __name__ == '__main__':
    main()

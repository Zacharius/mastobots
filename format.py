#!/usr/bin/python3

import re
import html2text

def formatStatus(rssEntry, extra):
    status = rssEntry.summary
    status = htmlToMastodonFormat(status)
#    status = removeInternalNewlines(status)
    #status = stripNaturalLink(status)
    status = concatAndInsertLink(status, rssEntry, extra)
    return status
    
#concats to make space for link and whatever else we want to append
def concatAndInsertLink(status, rssEntry, extra):
    maxStatusLen = 500
    statusLen = len(status)
    headerLen = len(rssEntry.title)
    extraLen = len(extra)
    #mastodon only counts the first 30 chars of a link towards its status limit,
    #the other 2 are for newlines before the link
    totalLen = statusLen+headerLen+32+extraLen

    if totalLen <= maxStatusLen:
        status += '\n\n'
    else:
        shortenedStatusLen = statusLen - (totalLen - maxStatusLen) - 3
        status = status[: shortenedStatusLen]
        status += '...\n\n'

    status += rssEntry.link
    status += extra
    return status
        
def removeInternalNewlines(status):
    status = status.replace("\n", " ")
    return status

def htmlToMastodonFormat(status):
    status = html2text.html2text(status)
    return status

    
def extractExternalLinks(text):
    linkRegEx = r'href="https?://(.*?)"'
    externalLinkRegEx = r'refactorcamp.org'

    links = re.findall(linkRegEx, text)
    externalLinks = []

    for link in links:
        if not re.match(externalLinkRegEx, link):
            externalLinks.append(link)

    return externalLinks

def stripHtml(text):
    stripHtmlRegEx = r'<.*?>'
    text = re.sub(stripHtmlRegEx, '', text)
    return text


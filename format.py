#!/usr/bin/python3

from re import findall, match, finditer, sub
import logging
import html2text

def formatStatus(rssEntry, extra):
    status = rssEntry.summary
    status = htmlToMastodonFormat(status)
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
        
def htmlToMastodonFormat(status):
    status = html2text.html2text(status)
    return status

def extractExternalLinks(text):
    linkRegEx = r'href="https?://(.*?)"'
    externalLinkRegEx = r'refactorcamp.org'

    links = findall(linkRegEx, text)
    externalLinks = []

    for link in links:
        if not match(externalLinkRegEx, link):
            externalLinks.append(link)

    return externalLinks

#grabs all text after the first <p> and before the first <a tag
def extractText(html):
#    logging.basicConfig(level=logging.DEBUG)
    extractTextRegEx = r'<p>(.*?)<a'
    extractTagsRegEx = r'<.+?><.+?>'

    text = match(extractTextRegEx, html).group(1)
    if not text:
        text = ''

    text = sub(extractTagsRegEx, ' ', text)

    return text


def formatBlogLog(title, author, link):
    blogLog = (title +
    ' by <a href="https://refactorcamp.org/' +
    author +
    '">' +
    author +
    '</a>. <a href="' +
    link +
    '">Link</a>')

    return blogLog

def formatLinkedTootLog(text, author):
    externalLinks = extractExternalLinks(text)
    title = extractText(text)
    
    formatString = title + '.'
    for link in externalLinks:
        formatString += '<a href="http://' + link + '">Link</a>. '
    formatString += ('ht <a href="https://refactorcamp.org/@' +
                      author + '">@' + author + '</a>')
    return formatString

def formatLocalTootLog(text, author):
    title = extractText(text)

    formatString = (title + ' -- <a href="https://refactorcamp.org/@' +
                      author + '">@' + author + '</a>')
    return formatString

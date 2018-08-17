#!/usr/bin/python3 
from mastodon import Mastodon
from logger import Logger
#mastodon docs: https://mastodonpy.readthedocs.io/en/latest/
from parser import Parser
from format import formatStatus
import os

def stallminator():

    feedURL = ['https://stallman.org/rss/rss.xml']

    stallminator = Mastobot('zach.faddis@gmail.com',
                            os.environ['STALLMINATOR_PASSWORD'],
                            'stallminator_clientcred.secret',
                            'stallminator_usercred.secret',
                            'https://mastodon.social').login()
    
    parser = Parser(feedURL)
    rssEntries = parser.getNewPosts()

    if len(rssEntries) > 5:
        rssEntries = rssEntries[:5]

    for entry in rssEntries:
        status = formatStatus(entry, "")
        print(entry.title)
        print(status)
        print('----------------------')
        stallminator.status_post(
            status,
            spoiler_text=entry.title,
            visibility="public")  


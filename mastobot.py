#!/usr/bin/python3 
from mastodon import Mastodon
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

def rbu_rss():

    blogs = {'https://www.ribbonfarm.com/feed/': '@vgr',
             'https://meaningness.com/rss.xml': '@meaningness',
             'http://feeds.akkartik.name/kartiks-scrapbook': '@akkartik@mastodon.social',
             'https://swellandcut.com/feed/': '@msweet',
             'https://www.spectology.com/feed.xml' : '@strangeattractor',
             'https://clutchofthedeadhand.com/rss/': '@johnhenry' }


    rbu_rss = Mastobot('zach@refactorcamp.org',
                      os.environ['STALLMINATOR_PASSWORD'],
                      'rbu_clientcred.secret',
                       'rbu_usercred.secret',
                       'https://refactorcamp.org').login()

    for feed in blogs:
        print(feed)
        parser = Parser([feed])
        rssEntries = parser.getNewPosts()

        for entry in rssEntries:
            status = formatStatus(entry,'\n'+blogs[feed] )
            print(entry.title)
            print(status)
            print('----------------------')
            rbu_rss.status_post(
                status,
               spoiler_text=entry.title,
              visibility="public")  

class Mastobot:
    SECRET_DIR = '/home/z/prj/mastobots/secrets/'

    def __init__(self, email, password, clientIDFile, accessTokenFile, url):
        self.email = email
        self.password = password
        self.clientIDFile = clientIDFile
        self.accessTokenFile = accessTokenFile
        self.url = url

        
    def login(self):
        access = Mastodon(
            client_id = self.SECRET_DIR + self.clientIDFile,
            api_base_url = self.url)

        access.log_in(
            self.email,
            self.password,
            to_file = self.SECRET_DIR + self.accessTokenFile)

        mastobot = Mastodon(
            access_token = self.SECRET_DIR + self.accessTokenFile,
            api_base_url = self.url)

        return mastobot

if __name__ == '__main__':
    stallminator()
    rbu_rss()

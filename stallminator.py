#!/usr/bin/python3 
from mastodon import Mastodon
#mastodon docs: https://mastodonpy.readthedocs.io/en/latest/
from parser import Parser
from format import formarStatus
import os

def stallminator():

    feedurl = ['https://stallman.org/rss/rss.xml']

    stallminator = Mastodon('zach.faddis@gmail.com',
                            os.environ['STALLMINATOR_PASSWORD'],
                            'stallminator_clientcred.secret',
                            'stallminator_usercred.secret').login()
    
    parser = Parser(feedURLList)
    rssEntries = parser.getNewPosts()

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
    
class Mastobot:
    SECRET_DIR = '/home/z/prj/mastobots/secrets/'

    def __init__(self, email, password, clientIDFile, accesTokenFile):
        self.email = email
        self.password = password
        self.clientIDFile = clientIDFile
        self.accessTokenFile = accessTokenFile

        
    def login():
        access = Mastodon(
            client_id = SECRET_DIR + clientIDFile)

        access.log_in(
            email,
            password,
            to_file = SECRET_DIR + accessTokenFile)

        stallminator = Mastodon(
            access_token = SECRET_DIR + accessTokenFile)

        return stallminator

if __name__ == '__main__':
    stallminator()

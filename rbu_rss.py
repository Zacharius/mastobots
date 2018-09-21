#!/usr/bin/python3

from mastodon import Mastodon
import os
from logger import Logger
from parser import Parser
from format import formatStatus
from util import getAbsolutePath

class RBU_RSS(Mastodon):
    SECRET_DIR = getAbsolutePath(__file__, 'secrets/')
    email = 'zach@refactorcamp.org'
    password = os.environ['STALLMINATOR_PASSWORD']
    clientIDFile = 'rbu_clientcred.secret'
    accessTokenFile = 'rbu_usercred.secret'
    instanceURL =  'https://refactorcamp.org'


    blogs = {'https://www.ribbonfarm.com/feed/': '@vgr',
             'http://feeds.akkartik.name/kartiks-scrapbook': '@akkartik@mastodon.social',
             'https://meaningness.com/rss.xml': '@meaningness',
             'https://swellandcut.com/feed/': '@msweet',
             'https://www.spectology.com/feed.xml' : '@adrianryan',
             'https://clutchofthedeadhand.com/rss/': '@johnhenry',
             'http://meltingasphalt.com/feed/' : "Kevin Simler",
             'https://subpixel.space/feed.xml' : '@telos',
             'https://kneelingbus.net/feed/' : "Drew Austin",
             'https://omniorthogonal.blogspot.com/feeds/posts/default' : "omniorthogonal",
             'http://thesublemon.tumblr.com/rss' : "thesublemon",
             'https://us1.campaign-archive.com/feed?u=78cbbb7f2882629a5157fa593&id=6b80b6e8da'
             : "@vgr",
             'http://zenpundit.com/?feed=rss2' : "zenpundit",
             'https://srconstantin.wordpress.com/feed/' : "srconstantin" ,
             'https://putanumonit.com/feed/' : 'putanumonit',
             'https://feeds.feedburner.com/Growwiser' : 'grow wiser',
             'https://josephckelly.com/feed/' : 'Joseph Kelly',
             'https://gravityandlevity.wordpress.com/feed/' : 'Brian Skinner',
             'https://www.nousmachina.net/rss/' : '@hewhocutsdown',
             'https://www.howell.io/rss.xml' : '@dehowell' ,
             'https://scottwernerd.com/feed/' : '@scottwerner',
             'http://secondforge.com/atom.xml' : '@jamescgibson',
             'https://ariel-greenwood-e07u.squarespace.com/new-blog?format=rss':
             'Ariel Greenwood',
             'http://www.thehidinghand.com/feed' : '@stefanozorzi',
             'http://msls.net/feed/' : '@bkam',
             'https://medium.com/feed/@j_camachor/' : '@jcamachor@mastodon.social',
             'https://www.digital-orrery.com/index.xml' : '@neocopinus',
             'https://goingferalco.wordpress.com/feed/' : '@james'}


    logDir = getAbsolutePath(__file__, 'log/')
    logfile = 'out.txt'

    def __init__(self):
        #super().__init__(
        #    access_token = self.SECRET_DIR + self.accessTokenFile,
        #    api_base_url = self.instanceURL)

        self.logger = Logger(self.logDir, self.logfile)
        self.__log_in_new_client()
        

    def run(self):
        self.__logAndPostFeeds()
        self.__logAndBoostHashtagSinceLastTime('heyfeedfox')

    def __log_in_new_client(self):
        super().__init__(
            client_id = self.SECRET_DIR + self.clientIDFile,
            api_base_url = self.instanceURL)

        self.log_in(
            self.email,
            self.password,
            to_file = self.SECRET_DIR + self.accessTokenFile)
        
    def __logAndPostFeeds(self):
        
        for feed in self.blogs:
            parser = Parser([feed])
            rssEntries = parser.getNewPosts()


            for entry in rssEntries:
                self.__postRSSEntry(entry, self.blogs[feed])
                self.logger.logBlog(entry.title, self.blogs[feed], entry.link)


    def __postRSSEntry(self, entry, author):
        status = formatStatus(entry,'\n'+ author)
        self.status_post(
            status,
            spoiler_text=entry.title,
            visibility="public")

    def __logAndBoostHashtagSinceLastTime(self, hashtag):
        latestID = self.__findLastRecordedHashtagID(hashtag)
        
        tagged_posts = self.timeline_hashtag(hashtag,
                                             local='true',
                                             since_id = latestID)
        for post in tagged_posts:
            if post.in_reply_to_id:
                post = self.__getParentPost(post)
            self.status_reblog(post.id)
            self.logger.logToot(post.content, post.account.acct)

        if len(tagged_posts) > 0:
            lastID = tagged_posts[0].id
            self.__saveLastRecordedHashtagID(hashtag, lastID)

    def __getParentPost(self, post):
        parentID = post.in_reply_to_id
        parentPost = self.status(parentID)
        return parentPost

    def __findLastRecordedHashtagID(self, hashtag):

        hashfile = getAbsolutePath(__file__, hashtag)
        
        try:
            with open(hashfile) as file:
                id = file.read()
        except:
            id = None

        return id

    def __saveLastRecordedHashtagID(self, hashtag, id):

        hashfile = getAbsolutePath(__file__, hashtag)

        with open(hashfile, "w") as file:
            file.write(str(id))
        

if __name__ == '__main__':
    rbu_rss = RBU_RSS()
    rbu_rss.run()

#!/usr/bin/python3

from mastodon import Mastodon
import os
from logger import Logger
from parser import Parser
from format import formatStatus

class RBU_RSS(Mastodon):
    SECRET_DIR = '/home/z/prj/mastobots/secrets/'
    email = 'zach@refactorcamp.org'
    password = os.environ['STALLMINATOR_PASSWORD']
    clientIDFile = 'rbu_clientcred.secret'
    accessTokenFile = 'rbu_usercred.secret'
    instanceURL =  'https://refactorcamp.org'


    blogs = {'https://www.ribbonfarm.com/feed/': '@vgr',
             'https://meaningness.com/rss.xml': '@meaningness',
             'http://feeds.akkartik.name/kartiks-scrapbook': '@akkartik@mastodon.social',
             'https://swellandcut.com/feed/': '@msweet',
             'https://www.spectology.com/feed.xml' : '@adrianryan',
             'https://clutchofthedeadhand.com/rss/': '@johnhenry',
             'http://meltingasphalt.com/feed/' : "Kevin Simler",
             'https://subpixel.space/feed.xml' : '@telos',
             'https://kneelingbus.net/feed/' : "Drew Austin",
             'https://omniorthogonal.blogspot.com/feeds/posts/default' : "",
             'http://thesublemon.tumblr.com/rss' : "",
             'https://us1.campaign-archive.com/feed?u=78cbbb7f2882629a5157fa593&id=6b80b6e8da'
             : "@vgr",
             'http://zenpundit.com/?feed=rss2' : "",
             'https://srconstantin.wordpress.com/feed/' : "" ,
             'https://putanumonit.com/feed/' : '',
             'https://feeds.feedburner.com/Growwiser' : '',
             'https://josephckelly.com/feed/' : 'Joseph Kelly',
             'https://gravityandlevity.wordpress.com/feed/' : 'Brian Skinner',
             'https://www.nousmachina.net/rss/' : '@hewhocutsdown',
             'https://www.howell.io/rss.xml' : '@dehowell' ,
             'https://scottwernerd.com/feed/' : '@scottwerner',
             'http://secondforge.com/atom.xml' : '@jamescgibson',
             'https://ariel-greenwood-e07u.squarespace.com/new-blog?format=rss':
             'Ariel Greenwood',
             'http://www.thehidinghand.com/feed' : '@stefanozorzi',
             'https://goingferalco.wordpress.com/feed/' : '@james'}


    logDir = '/home/z/prj/mastobots/log/'
    logfile = 'out.txt'
    logger = Logger(logDir, logfile)

    def __init__(self):
        super().__init__(
            access_token = self.SECRET_DIR + self.accessTokenFile,
            api_base_url = self.instanceURL)
        

    def run(self):
        self.__logAndPostFeeds()
        self.__logAndBoostHashtag('heyfeedfox')

    def __logAndPostFeeds(self):
        
        for feed in self.blogs:
            parser = Parser([feed])
            rssEntries = parser.getNewPosts()

            for entry in rssEntries:
                self.__postRSSEntry(entry, self.blogs[feed])
                self.logger.logBlog('', entry.title, self.blogs[feed], entry.link)


    def __postRSSEntry(self, entry, author):
        status = formatStatus(entry,'\n'+ author)
        self.status_post(
            status,
            spoiler_text=entry.title,
            visibility="public")

    def __logAndBoostHashtag(self, hashtag):
        tagged_posts = self.timeline_hashtag(hashtag, local='true')

        for post in tagged_posts:
            self.status_reblog(post.id)
            self.logger.logToot(post.content, post.account.acct)

if __name__ == '__main__':
    rbu_rss = RBU_RSS()
    rbu_rss.run()
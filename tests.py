#!/usr/bin/python3
import format
import unittest
from rbu_rss import RBU_RSS
from util import getAbsolutePath

class testFormat(unittest.TestCase):

    def setUp(self):
            self.maxDiff = None
            

    def test_extractText(self):
        testHtml = ('<p>The past was not as smelly as you think'
        '<a href="https://newrepublic.com/article/129828/'
        'getting-clean-tudor-way" rel="nofollow noopener" '
        'target="_blank"><span class="invisible"></span><span class='
        '"ellipsis"></span><span class="invisible"></span></a></p><p>'
        '<a href="https://refactorcamp.org/tags/heyfeedfox" '
        'class="mention hashtag" rel="tag"><span></span></a></p>')
        desiredResult = 'The past was not as smelly as you think' 
        
        result = format.extractText(testHtml)
        self.assertEqual(result, desiredResult)

    def test_extractExternalLinks(self):
       testHtml = ('<p>Design thinking is inherently conservative '
       '<a href="https://refactorcamp.org/tags/heyfeedfox" '
       'class="mention hashtag" rel="tag">#<span>heyfeedfox</span></a> '
       '<a href="https://hbr.org/2018/09/design-thinking-is-fundamentally'
       '-conservative-and-preserves-the-status-quo" rel="nofollow noopener"'
       'target="_blank"><span class="invisible">https://zfadd.is/resume'
       '</span><span class="ellipsis">hbr.org/2018/09/design-thinkin</span>'
       '<span class="invisible">g-is-fundamentally-conservative-and-preserves'
       '-the-status-quo</span></a></p>'
       'a href="http://hello world"')
       
       desiredResult = \
       ["hbr.org/2018/09/design-thinking-is-fundamentally-conservative-and-preserves-the-status-quo",
        "hello world"]

       result = format.extractExternalLinks(testHtml)
       self.assertEqual(result, desiredResult)

    def test_formatBlogLog(self):
        self.maxDiff = None
        title = 'Report: The Diminishing Marginal Value of Aesthetics'
        author = '@telos'
        link = 'http://subpixel.space/entries/diminishing-marginal-aesthetic-value/'
        result = format.formatBlogLog(title, author, link)

        desiredResult = (
            'Report: The Diminishing Marginal Value of Aesthetics '
            'by <a href="https://refactorcamp.org/@telos">@telos</a>. '
            '<a '
            'href="http://subpixel.space/entries/diminishing-marginal-aesthetic-value/">Link</a>')

        self.assertEqual(result, desiredResult)

    def test_formatLinkedTootLog(self):
        mastobot = RBU_RSS()
        linkedToot = mastobot.status(100722130702281095)

        title = linkedToot.content
        author = linkedToot.account.acct
        result = format.formatLinkedTootLog(title, author)

        desiredResult = ('A detailed assault on the book Sapiens. '
                         'The author of the critique cites his own work '
                         'a lot, but shows how many of the theories put forth '
                         'as fact in Sapiens are incorrect and ahistorical. .'
                         '<a '
                         'href="http://www.newenglishreview.org/custpage.cfm?'
                         'sec_id=189085">Link</a>. ht '
                         '<a href="https://refactorcamp.org/@britt">@britt</a>')

        self.assertEqual(result, desiredResult)

    def test_formatLocalTootLog(self):
        mastobot = RBU_RSS()
        localToot = mastobot.status(100719517294830106)

        title = localToot.content
        author = localToot.account.acct
        result = format.formatLocalTootLog(title, author)

        desiredResult = ('Irreversible choices have 2 aspects besides not '
                         'being able to go back: the fateful option leading '
                         'to uncharted regimes, and do-overs being'
                         ' costly/impossible. '
                         'If future is like past, or you can do-over cheaply'
                         ', irreversibility is moot. Like Coke vs Sprite at a '
                         'vending machine.'
                         '  -- <a href="https://refactorcamp.org/@vgr">@vgr</a>')

        self.assertEqual(result, desiredResult)
        
       
if __name__ == '__main__':
    unittest.main()

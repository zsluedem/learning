import feedparser
import re

def getwordcount(url):
    d = feedparser.parse(url)
    print d

getwordcount('http://blog.outer-court.com/rss.xml')
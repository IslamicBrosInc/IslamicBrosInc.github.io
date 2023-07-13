from pytube import YouTube
import scrapetube
from pymongo import MongoClient
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import langid





client = MongoClient('localhost', 27017)
db = client['cardbase'] 
videodb = client['videos']
urldbb = client['urls']
urlcollection = urldbb['url']
videocollection = db['videos']
collection = db['cards']

VIDEO_LIMIT_IN_SECONDS = 400

videos = scrapetube.get_channel("UCWsdcrre0WbCWML_PnuzoAg")



for video in videos:
    url = "https://www.youtube.com/watch?v="+str(video['videoId'])
    session = HTMLSession()
    yt = YouTube(url)
    length = yt.length
    resp = session.get(url)
    soup = bs(resp.html.html, "html.parser")
    title = soup.find("meta", itemprop="name")['content']
    lang = langid.classify(title)[0]
    if length<=VIDEO_LIMIT_IN_SECONDS and lang=='en':
        url_data = {
        'url': url,
        }
        urlcollection.insert_one(url_data)


# CODE TO UPDATE/ADD FIELDS TO PREXISTING DATA IN DATABASE
# urls = urlcollection.find()
# for oneurl in urls:
#     currurl = oneurl['url']
#     vidID = currurl[32:len(currurl)]
#     embed = "https://www.youtube.com/embed/" + vidID
#     filter = { 'url' : currurl }
#     urlembed = { "$set" : { 'embedurl': embed } }
#     urlcollection.update_one(filter,urlembed)
    

    
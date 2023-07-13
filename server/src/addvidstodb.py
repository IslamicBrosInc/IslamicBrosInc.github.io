from Get_Video_Explanation import *
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import *
from flask.json import jsonify
import simplejson as json 




app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/cardbase"
mongo = PyMongo(app)
client = MongoClient('localhost', 27017)
db = client['cardbase'] 
videodb = client['videos']
urldbb = client['urls']
urlcollection = urldbb['url']
videocollection = db['videos']
cardcollection = db['cards']


def setup(FatwaCard):
    FatwaCard.set_title_and_filename()
    FatwaCard.set_transcript()
    # FatwaCard.set_summary()
    # FatwaCard.remove_video_from_server()



#access video collection
videos = urlcollection.find()

ctr=0
for video in videos:
    ctr+=1
    urlID = video.get('cardID')
    url = video.get('url')

    card = FatwaCard(url)
    setup(card)
    title = card.get_title_and_filename()[0]
    # summary = card.get_summary()
    transcript_text = card.get_transcript()
    url = card.url
    betastatus = card.get_betastatus()
    card.set_cardID(ctr)
    author = card.author
    video_data = {
        'title': title,
        # 'summary': summary,
        'transcript': transcript_text,
        'video_url': url,
        'author':author,
        'cardID':ctr,
        'beta_status':betastatus
    }
    cardcollection.insert_one(video_data)
    print(card.get_cardID())

    if urlID ==200:
        break;


# cards = cardcollection.find()
# for card in cards:
#     currurl = card.get('video_url')
#     vidID = currurl[32:len(currurl)]
#     embed = "https://www.youtube.com/embed/" + vidID
#     filter = { 'video_url' : currurl }
#     urlembed = { "$set" : { 'vidembed': embed } }
#     cardcollection.update_one(filter,urlembed)
    


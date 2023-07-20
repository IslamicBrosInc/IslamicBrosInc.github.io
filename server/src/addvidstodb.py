from getenglish import *
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
laymanurl = urldbb['laymanurl']
videocollection = db['videos']
cardcollection = db['cards']
englishcollection = db['englishcards']
laymaneng = db['laymanenglish']

def setup(FatwaCard):
    FatwaCard.set_title_and_filename()
    FatwaCard.set_transcript()
    # FatwaCard.set_summary()
    # FatwaCard.remove_video_from_server()





#access video collection
videos = laymanurl.find()


def set_transcript(self):
    try:
        srt = YouTubeTranscriptApi.list_transcripts(self.url[32:len(self.url)])
        srt = srt.find_manually_created_transcript(['en'])

        for script in srt:
            if(script.is_generated==False):
                srt = script.find_manually_created_transcript(['en']).fetch()

        transcript_text = ""
        for line in srt:
                transcript_text+=line['text']
        self.transcript_text = transcript_text
    except youtube_transcript_api._errors.TranscriptsDisabled:
        try:    
            audio_file = YouTube(self.url).streams.filter(only_audio=True).first().download(filename=self.filename)
            model = whisper.load_model("tiny")
            result = model.transcribe(self.filename, language="en", fp16=False, verbose=True)
            transcript_text = result["text"]
            self.transcript_text = transcript_text
            self.remove_video_from_server()
            self.betastatus = True
        except:
            self.transcript_text = "Error"
            self.betastatus = False



ctr=0
for video in videos:
    ctr+=1
    urlID = video.get('cardID')
    url = video.get('url')
    embed = video.get('embed')
    title = video.get('title')
    card = FatwaCard(url,title)
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
        'embed':embed,
        'author':author,
        'cardID':ctr,
        'beta_status':betastatus,
        'question_status':card.isQuestion
    }
    laymaneng.insert_one(video_data)
    print(card.get_cardID())





# cards = laymaneng.find()
# for card in cards:
#     currurl = card.get('video_url')
#     vidID = currurl[32:len(currurl)]
#     embed = "https://www.youtube.com/embed/" + vidID
#     filter = { 'video_url' : currurl }
#     urlembed = { "$set" : { 'vidembed': embed } }
#     englishcollection.update_one(filter,urlembed)
    

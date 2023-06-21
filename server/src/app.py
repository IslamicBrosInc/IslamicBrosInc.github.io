from Get_Video_Explanation import *
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import *
import os
import scrapetube

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/cardbase"
mongo = PyMongo(app)
client = MongoClient('localhost', 27017)
db = client['cardbase'] 
videodb = client['videos']
videocollection = db['videos']
collection = db['cards']

def setup(FatwaCard):
    FatwaCard.set_title_and_filename()
    FatwaCard.set_transcript()
    FatwaCard.set_summary()
    FatwaCard.remove_video_from_server()


#access video collection
videos = videocollection.find()
ctr=0
for video in videos:
    ctr+=1
    url = video.get('url')
    card = FatwaCard(url)
    setup(card)
    title = card.get_title_and_filename()[0]
    summary = card.get_summary()
    transcript_text = card.get_transcript()
    url = card.url
    video_data = {
        'title': title,
        'summary': summary,
        'transcript': transcript_text,
        'video_url': url
    }
    collection.insert_one(video_data)
    print(ctr)



# url = "https://www.youtube.com/watch?v=-Q9BVvl7y-w"
# card = FatwaCard(url)


# setup(card)

# title = card.get_title_and_filename()[0]
# summary = card.get_summary()
# transcript_text = card.get_transcript()
# url = card.url


# video_data = {
#     'title': title,
#     'summary': summary,
#     'transcript': transcript_text,
#     'video_url': url
# }
# collection.insert_one(video_data)

                        
# # @app.route('/', methods=['GET', 'POST'])
# # def run():



# #     # Render template with data
# #     return render_template('index.html', title=title, summary=summary, transcript=transcript_text, video_url=url)

# if __name__ == '__main__':
#     # app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
#     documents = collection.find()
#     for document in documents:
#         print(document)
        
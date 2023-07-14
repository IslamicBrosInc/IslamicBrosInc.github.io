from Get_Video_Explanation import *
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import *
from flask.json import jsonify
import simplejson as json 
import os
import scrapetube

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/cardbase"
mongo = PyMongo(app)
client = MongoClient('localhost', 27017)
db = client['cardbase'] 
videodb = client['videos']
urldbb = client['urls']
urlcollection = urldbb['url']
videocollection = db['videos']
collection = db['cards']





                        
@app.route('/', methods=['GET', 'POST'])
def run():
    cards = collection.find()
    urls = urlcollection.find()
    card = collection.find_one({"cardID":"0"})

    # Render template with data
    return render_template('index.html',cards=cards, urls=urls,card=card)
# title=title, summary=summary, transcript=transcript_text, video_url=url


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    # documents = collection.find()
    # for document in documents:
    #     print(document)
        
from Get_Video_Explanation import *
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import *
from flask.json import jsonify
import simplejson as json 
import os
import scrapetube
import re
from encoder import CustomJSONEncoder

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/cardbase"
app.json_encoder = CustomJSONEncoder
mongo = PyMongo(app)
client = MongoClient('localhost', 27017)
db = client['cardbase'] 
videodb = client['videos']
urldbb = client['urls']
urlcollection = urldbb['url']
videocollection = db['videos']
collection = db['cards']
englishcollection = db['englishcards']
laymancollection = db['laymanenglish']


                        
@app.route('/', methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        data = request.get_json()
        query = data.get("query", "")
        print(query)
        regex_pattern = re.compile(f".*{query}.*", re.IGNORECASE)

        search = {"title": {"$regex": query, "$options": "i"}}
        results = laymancollection.find(search)
        print("results", results)

        search_results = list(results)

        print(search_results)

        return jsonify(search_results)
    else:
        cards = laymancollection.find()

        card_list = list(cards)
        return render_template('index.html', cards=card_list)







if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    # documents = collection.find()
    # for document in documents:
    #     print(document)
    
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import *
from flask.json import jsonify
from bson import ObjectId
import simplejson as json 
import os
import scrapetube
import re
# from encoder import CustomJSONEncoder


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)
    

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
        # print(query)
        regex_pattern = re.compile(f".*{query}.*", re.IGNORECASE)

        search = {"transcript": {"$regex": query, "$options": "i"}}
        results = laymancollection.find(search)

        # Convert MongoDB documents to Python dictionaries
        search_results = [result for result in results]

        # Serialize ObjectId to string manually
        for result in search_results:
            result["_id"] = str(result["_id"])

        return jsonify(search_results)
    else:
        # print('tmgan')
        cards = laymancollection.find()
        card_list = [card for card in cards]

        return render_template('index.html', cards=card_list, query=None)








if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    # documents = collection.find()
    # for document in documents:
    #     print(document)
    
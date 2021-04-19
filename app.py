from flask import Flask, request, jsonify, render_template
import json
import pymongo
import os
from dotenv import load_dotenv
from bson.json_util import dumps

load_dotenv()

app = Flask(__name__,template_folder='.')

print(os.getenv("MONGO_URI"))

client = pymongo.MongoClient(os.getenv("MONGO_URI"))

dict_db = client["database"]

dictionary = dict_db["dictionary"]

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/add',methods=['POST'])
def dict_add():
	word_dict = dict()

	try:
		word_dict['word'] = request.form['word']
		word_dict['definition'] = request.form['definition']
	except:
		word_dict = request.get_json()

	word_dict['word'] = word_dict['word'].lower()

	res = dictionary.find_one({"word":word_dict['word']})

	if res==None:
		id = dictionary.insert_one(word_dict)
		return {"success":"word added"}
	else:
		return {"error":"word already exists in dictionary"}
		

@app.route('/update',methods=['POST'])
def dict_update():
	word_dict = dict()

	try:
		word_dict['word'] = request.form['word']
		word_dict['definition'] = request.form['definition']
	except:
		word_dict = request.get_json()
		
	word_dict['word'] = word_dict['word'].lower()

	query = { "word": word_dict['word'] }
	newvalues = { "$set": word_dict }

	res = dictionary.update_one(query, newvalues)

	if res.modified_count:
		return {"success":"word updated"}
	else:
		return {"error":"word not found to be updated"}

@app.route('/find',methods=['GET'])
def dict_find():
	try:
		word = request.args.get('word').lower()
	except:
		word = None

	try:
		regex = not (request.args.get('regex')=='False')
	except:
		regex = True

	if word == None or word == "" :
		res = dictionary.find().sort("word")
	elif regex:
		res = dictionary.find({'word':{'$regex':word}}).sort("word")
	else:
		res = dictionary.find({'word':word})

	return dumps(list(res))

@app.route('/delete',methods=['GET'])
def dict_delete():
	word = request.args.get('word').lower()

	query = { "word": word }

	x = dictionary.delete_one(query)
	if x.deleted_count:
		return {'success':'word deleted'}
	else:
		return {'error': 'word does not exist'}


if __name__ == '__main__':
	app.run(debug=True)
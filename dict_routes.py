from flask import request
from bson.json_util import dumps
from auth import token_required
import os
import jwt
import re

def create_dict_routes(app,db):
	dictionary = db["dictionary"]

	@app.route('/update',methods=['POST'])
	@token_required
	def dict_add():
		email = jwt.decode(request.headers['TOKEN'],os.getenv("SECRET_KEY"), algorithms=['HS256'])['email']
		word_dict = request.get_json()
		print(word_dict)
		word_dict['word'] = word_dict['word'].lower()

		res =  dictionary.find_one({'user':email,'dictionary.word':word_dict['word']},{'_id': 0, 'dictionary': {'$elemMatch': {'word': word_dict['word']}}})

		if res==None:
			id = dictionary.update_one({'user': email}, {'$push': {'dictionary': word_dict}})
			return {"success":"word added"}
		else:
			query = { 
			"user": email,
			'dictionary.word':word_dict['word']
			}

			word_dict = {
			'dictionary.$.word':word_dict['word'],
			'dictionary.$.definition':word_dict['definition']
			}

			newvalues = { "$set": word_dict }

			res = dictionary.update_one(query, newvalues)

			if res.modified_count:
				return {"success":"word updated"}
		return {"error":"an error occurred"}
			

	@app.route('/find',methods=['GET'])
	@token_required
	def dict_find():
		email = jwt.decode(request.headers['TOKEN'],os.getenv("SECRET_KEY"), algorithms=['HS256'])['email']

		try:
			word = request.args.get('word').lower()
		except:
			word = None

		try:
			regex = not (request.args.get('regex')=='False')
		except:
			regex = True

		if regex :
			res = dictionary.find_one({'user':email})['dictionary']
			if word !=None and word !="":
				res = list(filter(lambda x: re.search(word,x['word']) != None ,res))
		else:
			res = dictionary.find_one({'user':email,'dictionary.word':word},{'_id': 0, 'dictionary': {'$elemMatch': {'word': word}}})
			if(res == None):
				res = list()
			else:
				res = res['dictionary']

		res.sort(key = lambda x: x['word'])
		print(res)
		return dumps(res)

	@app.route('/delete',methods=['GET'])
	@token_required
	def dict_delete():
		email = jwt.decode(request.headers['TOKEN'],os.getenv("SECRET_KEY"), algorithms=['HS256'])['email']

		word = request.args.get('word').lower()

		query = { "word": word }

		x = dictionary.update_one({'user': email},{'$pull': { 'dictionary': query }})
		print(x)
		if x.modified_count:
			return {'success':'word deleted'}
		else:
			return {'error': 'word does not exist'}

	return app

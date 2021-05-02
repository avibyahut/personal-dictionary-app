from flask import request, make_response
import bcrypt
import jwt
import os
import datetime

def create_auth_routes(app,db):
	users = db['users']
	dictionary = db["dictionary"]

	@app.route('/register',methods=['POST'])
	def register_user():
		user = request.get_json()

		if 'email' not in user or 'username' not in user or 'password' not in user:
			return {"error":"invalid data provided"}

		res = users.find_one({"email":user['email']})
		
		if res == None:
			user['password'] = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt(rounds=10)).decode()
			id = users.insert_one(user)
			new_dict = {
			'user':user['email'],
			'dictionary':[]
			}
			id = dictionary.insert_one(new_dict)
			return {"success":"User successfully regitered"}, 201
		else:
			return {"error":"email already registered"}


	@app.route('/login',methods=['POST'])
	def login_user():
		user = request.get_json()

		if 'email' not in user or 'password' not in user:
			return {"error":"invalid data provided"}

		res = users.find_one({"email":user['email']})

		if res != None and bcrypt.checkpw(user['password'].encode('utf-8'),res['password'].encode('utf-8')):
			payload = {
			'email': user['email'],
			'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
 			}
			token = jwt.encode(payload,os.getenv("SECRET_KEY"))
			return {"loggedIn":True,'username': res['username'],'token':token}, 202
		else:
			return {"error":"UserName or Password is wrong"}

	@app.route('/check_login',methods=['GET'])
	def check_login_user():
		if('TOKEN' in request.headers):
			try:
				email = jwt.decode(request.headers['TOKEN'],os.getenv("SECRET_KEY"), algorithms=['HS256'])['email']
				res = users.find_one({"email":email})
				if res!=None:
					return {"loggedIn":True,'username': res['username']}
				else:
					return {"loggedIn":False}
			except Exception as e:
				print(str(e))
				return {"loggedIn":False}
		else:
			return {"loggedIn":False}

	return app

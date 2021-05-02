import jwt
import os
from flask import request

def token_required(func):
	def wrap(*args, **kwargs):
		try:
			if request.headers['TOKEN'] != '' and request.headers['TOKEN'] != None:
				try:
					data = jwt.decode(request.headers['TOKEN'],os.getenv("SECRET_KEY"), algorithms=['HS256'])
					print("token verified")
					return func(*args, **kwargs)
				except jwt.exceptions.ExpiredSignatureError:
					return {"error":"token expired"}
				except Exception as e:
					print(str(e))
					return {"error":"invalid token"}
			else:
				return {"error":"token required"}
		except:
			return {"error":"an error occurred"}

	wrap.__name__ = func.__name__

	return wrap


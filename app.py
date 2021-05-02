from flask import Flask, render_template, make_response
from flask_cors import CORS
import pymongo
import os
import secrets
import string
from dotenv import load_dotenv
from dict_routes import create_dict_routes
from auth_routes import create_auth_routes

load_dotenv()

client = pymongo.MongoClient(os.getenv("MONGO_URI"))

db = client["database"]

app = Flask(__name__,template_folder='.')
CORS(app)
create_dict_routes(app,db)
create_auth_routes(app,db)

@app.route('/')
def index():
	resp = make_response(render_template('index.html'))
	return resp

@app.route('/test')
def test():
	resp = make_response()
	resp.set_cookie("name","abhinav")
	return resp

if __name__ == '__main__':
	app.run(debug=True)
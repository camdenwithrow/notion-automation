from email import message
from multiprocessing.sharedctypes import Value
from flask import Flask, jsonify, request, make_response
import os
from dotenv import load_dotenv
import json

from notion import NotionApi

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
TODO_ID = os.getenv("TODO_ID")

app = Flask(__name__)

@app.route('/')
def index():
    return make_response(jsonify(message="notion quick add api"), 200)

@app.route('/health')
def health():
    return make_response(jsonify(message="healthy"), 200)


if __name__ == '__main__':
    app.run()

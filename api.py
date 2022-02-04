from flask import Flask, jsonify, request, make_response
import os
from dotenv import load_dotenv
import json
import requests

from notion import NotionApi

load_dotenv()

AUTH_KEY = os.getenv("AUTH_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
TODO_LIST_ID = os.getenv("TODO_LIST_ID")

app = Flask(__name__)


def create_resp(message: str, status: int, **kwargs):
    return make_response(jsonify(message=message, status=status, **kwargs), status)


def auth(headers):
    return headers.get("Authorization") == "Bearer " + AUTH_KEY


@app.route('/', methods=['GET'])
def index():
    return make_response(jsonify(message="notion quick add api"), 200)


@app.route('/health', methods=['GET'])
def health():
    if not auth(request.headers): return create_resp(message="Unauthorized", status=401)
    return make_response(jsonify(message="healthy"), 200)


@app.route('/quicktodo', methods=['POST'])
def quicktodo():
    """add new todo into todo section from request"""
    if not auth(request.headers): return create_resp(message="Unauthorized", status=401)
    api = NotionApi(NOTION_API_KEY)
    response = None
    try:
        data = json.loads(request.data)
        todo = data['todo']

        # Create new todo block with request field 'todo'
        new_block = {
            "children": [{
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "text": [{"type": "text", "text": {"content": todo}}]
                }
            }]
        }

        # Request to append new todo to todo section
        update_resp = api.append_block_children(TODO_LIST_ID, new_block)
        update_resp.raise_for_status()
        results = json.loads(update_resp.content)["results"]
        response = create_resp(message="success", status=200, results=results)

    except ValueError:
        response = create_resp(message="JSON parse error", status=400, code="ValueError")
    except KeyError:
        response = create_resp(
            message="Request must include todo field", status=400, code="KeyError")
    except requests.exceptions.HTTPError as e:
        response = create_resp(message="Error: " + str(e), status=400)
    except Exception as e:
        response = create_resp(
            message="Something went wrong " + str(e), status=400)
    finally:
        return response


if __name__ == '__main__':
    app.run()

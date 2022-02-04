import os
from dotenv import load_dotenv
import json

from notion import NotionApi

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
TODO_LIST_ID = os.getenv("TODO_LIST_ID")

def delete_checked(api):
    todo_resp = api.get_block_children(TODO_LIST_ID, 100)
    todo_results = json.loads(todo_resp.content)['results']
    to_delete = [obj["id"] for obj in todo_results if obj["type"] == "to_do" and obj["to_do"]["checked"]]
    delete_resps = [api.delete_block(id) for id in to_delete]
    return delete_resps

def main():
    api = NotionApi(NOTION_API_KEY)
    delete_checked(api)

if __name__ == '__main__':
    main()
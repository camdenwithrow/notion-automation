import os
from dotenv import load_dotenv
import json

from notion import NotionApi

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
TODO_LIST_ID = os.getenv("TODO_LIST_ID")
TOMORROW_LIST_ID = os.getenv("TOMORROW_LIST_ID")


def delete_checked(api):
    todo_resp = api.get_block_children(TODO_LIST_ID, 100)
    todo_results = json.loads(todo_resp.content)['results']
    to_delete = [
        obj["id"] for obj in todo_results
        if obj["type"] == "to_do" and obj["to_do"]["checked"]
    ]
    delete_resps = [api.delete_block(id) for id in to_delete]
    return delete_resps


def tomorrow_to_today(api):
    tomorrow_resp = api.get_block_children(TOMORROW_LIST_ID, 100)
    tomorrow_results = json.loads(tomorrow_resp.content)["results"]
    if tomorrow_results is not []:
        to_update = {
            "children": [
                {
                    "object": res["object"],
                    "type": "to_do",
                    "to_do": res["to_do"]
                }
                for res in tomorrow_results if res["type"] == "to_do"
            ]
        }
        update_resp = api.append_block_children(TODO_LIST_ID, to_update)

        to_delete = [res["id"] for res in tomorrow_results]

        delete_resp = [api.delete_block(id) for id in to_delete]

        return (update_resp, delete_resp)
    return None


def main():
    api = NotionApi(NOTION_API_KEY)
    tomorrow_to_today(api)
    delete_checked(api)


if __name__ == '__main__':
    main()

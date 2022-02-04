import os
from dotenv import load_dotenv
import json
import requests

from notion import NotionApi

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
TODO_LIST_ID = os.getenv("TODO_LIST_ID")
TOMORROW_LIST_ID = os.getenv("TOMORROW_LIST_ID")


def check_request(resp):
    """Checks request for 200 response"""
    try:
        # check resp status
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # non 200 response
        return "Error: " + str(e)


def delete_checked(api):
    """Deletes all todo blocks that are checked off in main todo list section"""
    todo_resp = api.get_block_children(TODO_LIST_ID, 100)
    check_request(todo_resp)

    # Load results from resp then find and delete all that are checked
    todo_results = json.loads(todo_resp.content)['results']
    to_delete = [
        obj["id"] for obj in todo_results
        if obj["type"] == "to_do" and obj["to_do"]["checked"]
    ]
    delete_resps = [api.delete_block(id) for id in to_delete]
    for resp in delete_resps:
        check_request(resp)

    return delete_resps


def tomorrow_to_today(api):
    """Moves all todo blocks in the tomorrow section to the main todo section 
    then deletes them from tomorrow section"""
    tomorrow_resp = api.get_block_children(TOMORROW_LIST_ID, 100)
    check_request(tomorrow_resp)

    tomorrow_results = json.loads(tomorrow_resp.content)["results"]
    # check if there are any results to update
    if tomorrow_results is not []:
        # create and updated blocks append to main todo section
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
        check_request(update_resp)

        # delete old blocks in tomorrow section
        to_delete = [res["id"] for res in tomorrow_results]

        delete_resps = [api.delete_block(id) for id in to_delete]
        for resp in delete_resps:
            check_request(resp)

        return (update_resp, delete_resps)
    return None


def main():
    api = NotionApi(NOTION_API_KEY)
    tomorrow_to_today(api)
    delete_checked(api)


if __name__ == '__main__':
    main()

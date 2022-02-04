import os
from dotenv import load_dotenv
import json
import requests
import schedule
import time

from notion import NotionApi

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
TODO_LIST_ID = os.getenv("TODO_LIST_ID")
TOMORROW_LIST_ID = os.getenv("TOMORROW_LIST_ID")
HABITS_LIST_ID = os.getenv("HABITS_LIST_ID")


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

def habit_tracker(api):
    """Uncheck completed habits and add them to habit tracker"""
    habit_resp = api.get_block_children(HABITS_LIST_ID, 100)
    check_request(habit_resp)

    habits_results = json.loads(habit_resp.content)["results"]
    for habit in habits_results:
        if habit["type"] == "to_do" and habit["to_do"]["checked"]:
            # uncheck habit
            update_resp = api.update_block(habit["id"], {"to_do": {"checked": False}})
            check_request(update_resp)

def main():
    api = NotionApi(NOTION_API_KEY)
    print("Running")
    tomorrow_to_today(api)
    delete_checked(api)
    habit_tracker(api)
    print("Run finished")


if __name__ == '__main__':
    # main()
    try:
        schedule.every().day.at("1:00").do(main)
        print("Starting, press Ctrl+C to exit")

        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Process exited")

import os
from dotenv import load_dotenv
import json

from notion import NotionApi

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")

def main():
    api = NotionApi(NOTION_API_KEY)

if __name__ == '__main__':
    main()
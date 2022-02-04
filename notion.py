import requests


class NotionApi:
    url = "https://api.notion.com/v1"

    def __init__(self, api_key):
        self.headers = {
            "Accept": "application/json",
            "Notion-Version": "2021-08-16",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(api_key),
        }

    def create_page(self, data):
        request_url = "{url}/pages".format(url=self.url)
        response = requests.request("POST", request_url, headers=self.headers, json=data)
        return response

    def get_block(self):
        response = requests.request("GET", self.url, headers=self.headers)
        return response

    def get_block_children(self, id, pages):
        request_url = "{url}/blocks/{id}/children?page_size={pages}".format(
            url=self.url, id=id, pages=pages
        )
        response = requests.request("GET", request_url, headers=self.headers)
        return response

    def delete_block(self, id):
        request_url = "{url}/blocks/{id}".format(url=self.url, id=id)
        response = requests.request("DELETE", request_url, headers=self.headers)
        return response

    def append_block_children(self, id, blocks):
        request_url = "{url}/blocks/{id}/children".format(url=self.url, id=id)
        response = requests.request(
            "PATCH", request_url, headers=self.headers, json=blocks
        )
        return response

    def update_block(self, id, payload):
        request_url = "{url}/blocks/{id}".format(url=self.url, id=id)
        response = requests.request(
            "PATCH", request_url, headers=self.headers, json=payload
        )
        return response
import requests
import json

def api_call(endpoint, headers):
    response = requests.get(endpoint, headers=headers)
    return json.loads(response.text)

def handle_query(query):
    pass

if __name__ == "__main__":
    while True:
        query = input("Ask me a question about GitHub API: ")
        handle_query(query)

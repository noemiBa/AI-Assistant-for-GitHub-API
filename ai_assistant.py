import os
import requests
import json
from transformers import GPTNeoForCausalLM, GPT2Tokenizer

class GPTNeoAssistant:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
        self.model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
    
    def generate_response(self, query):
        inputs = self.tokenizer.encode(query, return_tensors="pt", truncation=True)
        outputs = self.model.generate(inputs, max_length=150, temperature=0.7, pad_token_id=self.tokenizer.eos_token_id)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

class GitHubAPIHandler:
    def __init__(self, spec_url, spec_filename):
        self.spec_filename = spec_filename
        if not os.path.exists(spec_filename):
            self.download_api_spec(spec_url, spec_filename)
        self.load_spec(spec_filename)
    
    def download_api_spec(self, url, filename):
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)
    
    def load_spec(self, filename):
        with open(filename, 'r') as file:
            self.api_spec = json.load(file)
    
    def handle_query(self, query):
        if "authenticate" in query:
            return "To authenticate your requests, use the 'Authorization' header with your personal access token."

def handle_query(query):
    if "GitHub API" in query:
        response = github_api_handler.handle_query(query)
    else:
        response = gpt_neo_assistant.generate_response(query)
    print(response)

api_spec_url = 'https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json'
api_spec_filename = 'api_spec.json'

gpt_neo_assistant = GPTNeoAssistant()
github_api_handler = GitHubAPIHandler(api_spec_url, api_spec_filename)

if __name__ == "__main__":
    while True:
        query = input("Ask me a question: ")
        handle_query(query)
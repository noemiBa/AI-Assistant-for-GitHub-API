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
    
    def generate_api_response(self, info):
        if info:
            response_text = f"Path: {info['path']}\nMethod: {info['method']}\nSummary: {info['summary']}\nDescription: {info['description']}"
            return response_text
        else:
            return "I couldn't find relevant information for your query."

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

    # def print_spec_summary(self):
    #     print(f"Keys at the root level: {list(self.api_spec.keys())}")
    #     print(f"Keys under 'paths': {list(self.api_spec['paths'].keys())[:5]}")  # Print first 5 keys under 'paths'
    #     print(f"Details of one endpoint: {self.api_spec['paths']['/repos/{owner}/{repo}']}")
    
    def preprocess_query(self, query):  
        keywords = query.lower().split()
        return keywords

    def lookup_info(self, keywords):
        for path, operations in github_api_handler.api_spec['paths'].items():
            for method, operation in operations.items():
                if any(keyword in operation['description'].lower() for keyword in keywords):
                    return {
                        'path': path,
                        'method': method.upper(),
                        'summary': operation.get('summary', ''),
                        'description': operation.get('description', ''),
                        'parameters': operation.get('parameters', []),
                        'responses': operation.get('responses', {})
                    }
        return None
    
    def load_spec(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            self.api_spec = json.load(file)

def handle_query(query):
        keywords = github_api_handler.preprocess_query(query)  
        info = github_api_handler.lookup_info(keywords) 
        response = gpt_neo_assistant.generate_api_response(info)  
        print(response)

api_spec_url = 'https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json'
api_spec_filename = 'api_spec.json'

gpt_neo_assistant = GPTNeoAssistant()
github_api_handler = GitHubAPIHandler(api_spec_url, api_spec_filename)

if __name__ == "__main__":
    while True:
        query = input("Ask me a question: ")
        handle_query(query)
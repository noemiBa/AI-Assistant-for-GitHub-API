import os
import requests
import json
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
from fuzzywuzzy import process

class GPTNeoAssistant:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-125M")  
        self.model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")  
        self.pre_generated_responses = self.load_pre_generated_responses()

    def load_pre_generated_responses(self):
        with open('pre_generated_responses.json', 'r') as file:
            return json.load(file)
        
    def generate_response(self, query):
        inputs = self.tokenizer.encode(query, return_tensors="pt", truncation=True)
        outputs = self.model.generate(inputs, max_length=350, temperature=0.7, pad_token_id=self.tokenizer.eos_token_id)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    
    def get_closest_pre_generated_response(self, query):
        closest_match, score = process.extractOne(query, self.pre_generated_responses.keys())
        
        if score >= 80:
            return self.pre_generated_responses[closest_match]
        return None
    
    def generate_api_response(self, query, info):
        pre_generated_response = self.get_closest_pre_generated_response(query)
        if pre_generated_response:
            return pre_generated_response
        if info:
            input_text = f"User Query: {query}\nPath: {info['path']}\nMethod: {info['method']}\nSummary: {info['summary']}\nDescription: {info['description']}"
            return self.generate_response(input_text)
        else:
            return self.generate_response(query)

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
    #     print(f"Keys under 'paths': {list(self.api_spec['paths'].keys())[:5]}")  
    #     print(f"Details of one endpoint: {self.api_spec['paths']['/repos/{owner}/{repo}']}")
    
    def preprocess_query(self, query):  
        keywords = query.lower().split()
        return keywords

    def lookup_info(self, keywords):
        keywords_set = set(keywords)
        best_match = None
        best_match_score = 0
        for path, operations in self.api_spec['paths'].items():
            for method, operation in operations.items():
                description_words = set(operation['description'].lower().split())
                common_words = description_words.intersection(keywords_set)
                match_score = len(common_words)
                if match_score > best_match_score:
                    best_match_score = match_score
                    best_match = {
                        'path': path,
                        'method': method.upper(),
                        'summary': operation.get('summary', ''),
                        'description': operation.get('description', ''),
                        'parameters': operation.get('parameters', []),
                        'responses': operation.get('responses', {})
                    }
        return best_match
    
    def load_spec(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            self.api_spec = json.load(file)

def handle_query(query):
    print("Processing query...")
    keywords = github_api_handler.preprocess_query(query)
    print("Looking up info...")
    info = github_api_handler.lookup_info(keywords)
    print("Generating response...")
    response = gpt_neo_assistant.generate_api_response(query, info)
    print(response)

api_spec_url = 'https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json'
api_spec_filename = 'api_spec.json'

gpt_neo_assistant = GPTNeoAssistant()
github_api_handler = GitHubAPIHandler(api_spec_url, api_spec_filename)

if __name__ == "__main__":
    while True:
        query = input("Ask me a question: ")
        handle_query(query)
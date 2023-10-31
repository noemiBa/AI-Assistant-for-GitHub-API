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

gpt_neo_assistant = GPTNeoAssistant()


def api_call(endpoint, headers):
    response = requests.get(endpoint, headers=headers)
    return json.loads(response.text)


def handle_query(query):
    pass

if __name__ == "__main__":
    while True:
        query = input("Ask me a question about GitHub API: ")
        handle_query(query)

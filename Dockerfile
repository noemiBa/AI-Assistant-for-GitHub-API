FROM python:3.8-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir transformers requests torch fuzzywuzzy python-Levenshtein

EXPOSE 80

CMD ["python", "ai_assistant.py"]

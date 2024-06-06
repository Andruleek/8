import os
import json
import re

def search_by_name(query):
    pattern = re.compile(r'^name:(\w+)$')
    match = pattern.match(query)
    if match:
        author_name = match.group(1)
        return [q for q in quotes if q.author.name == author_name]
    else:
        return []

def search_by_tag(query):
    pattern = re.compile(r'^tag:(\w+)$')
    match = pattern.match(query)
    if match:
        tag = match.group(1)
        return [q for q in quotes if tag in q.tags]
    else:
        return []


class Author:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Quote:
    def __init__(self, text, tags=None, author=None):
        self.text = text
        self.tags = tags
        self.author = author

    @classmethod
    def search_by_tags(cls, query):
        return [q for q in quotes if query in q.tags]

    @classmethod
    def search_by_author(cls, query):
        return [q for q in quotes if q.author.name == query]

    @classmethod
    def search_by_tags_and_author(cls, query, author):
        return [q for q in quotes if query in q.tags and q.author.name == author]

model_map = {'author': Author, 'quote': Quote}
quotes = []
authors = []

def load_quotes():
    global quotes, authors
    if os.path.exists('quotes.json'):
        with open('quotes.json', 'r') as f:
            data = json.load(f)
        for author_data in data['authors']:
            author = Author(author_data['name'], author_data['age'])
            authors.append(author)
        for quote_data in data['quotes']:
            author = next((a for a in authors if a.name == quote_data['author']), None)
            quote = Quote(quote_data['text'], quote_data['tags'], author)
            quotes.append(quote)

load_quotes()

while True:
    command = input('Enter command: ')
    if command.startswith('name:'):
        author_name = command.split(':')[1].strip()
        results = [q for q in quotes if q.author.name == author_name]
        if results:
            print(f"Quotes by {author_name}:")
            for quote in results:
                print(quote.text)
        else:
            print(f"No quotes found for {author_name}")
    elif command.startswith('tag:'):
        tag = command.split(':')[1].strip()
        results = [q for q in quotes if tag in q.tags]
        if results:
            print(f"Quotes with tag {tag}:")
            for quote in results:
                print(quote.text)
        else:
            print(f"No quotes found with tag {tag}")
    elif command.startswith('tags:'):
        tags = command.split(':')[1].strip().split(',')
        results = [q for q in quotes if all(tag in q.tags for tag in tags)]
        if results:
            print(f"Quotes with tags {', '.join(tags)}:")
            for quote in results:
                print(quote.text)
        else:
            print(f"No quotes found with tags {', '.join(tags)}")
    elif command == 'exit':
        break
    else:
        print('Invalid command')
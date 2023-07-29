import os
import sys
from markdown_it import MarkdownIt
import requests

READWISE_API_KEY = os.getenv("READWISE_API_KEY")
READWISE_API_URL = 'https://readwise.io/api/v2/highlights/'

def extract_quotes_from_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    md = MarkdownIt()
    tokens = md.parse(content)
    quotes = []
    for i in range(len(tokens)):
        if tokens[i].type == 'blockquote_open':
            for j in range(i+1, len(tokens)):
                if tokens[j].type == 'inline':
                    quote_text = tokens[j].content.strip()
                    quotes.append(quote_text)
                    break
    return quotes


def upload_quote_to_readwise(quote, book_title):
    headers = {
        'Authorization': f'Token {READWISE_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'highlights': [
            {
                'text': quote,
                'title': book_title
            }
        ]
    }
    response = requests.post(READWISE_API_URL, json=data, headers=headers)
    return response

def print_upload_result(response, quote):
    if response.status_code == 200 or response.status_code == 201:
        print(f'Successfully uploaded quote: {quote}')
    else:
        print(f'Failed to upload quote: {quote}, status code: {response.status_code}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python readwise_md.py <folder_path> <prefix(The common characters at the beginning of your quote files)>)')
        sys.exit(1)

    folder_path = sys.argv[1]
    book_title = os.path.basename(folder_path)  # Using folder name as book title

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.md'):
                full_path = os.path.join(root, file)
                quotes = extract_quotes_from_markdown(full_path)
                for quote in quotes:
                    response = upload_quote_to_readwise(quote, book_title)
                    print_upload_result(response, quote)

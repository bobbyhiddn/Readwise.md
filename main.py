import os
import sys
import re
import shutil
import tempfile
from markdown_it import MarkdownIt
import requests

READWISE_API_KEY = 'MH27ZE7rlYwa2E4i8moa9zLTpIS9rcyQZukYVNnwsPBwKEW0mg'
READWISE_API_URL = 'https://readwise.io/api/v2/highlights/'
CHECKLIST_FILE = 'checklist.txt'

def scan_files(folder_path):
    files_to_upload = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if re.match(r'Pg\. \d+ - .*\.md', file):
                files_to_upload.append(os.path.join(root, file))
    return files_to_upload

def update_checklist_file(files_to_upload):
    if not os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE, 'w') as f:
            for file in files_to_upload:
                f.write(f'{file}\n')

def read_checklist_file():
    with open(CHECKLIST_FILE, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]

def mark_uploaded_file(file):
    with open(CHECKLIST_FILE, 'r') as f, tempfile.NamedTemporaryFile('w', delete=False) as tmp:
        for line in f:
            if line.strip() == file:
                tmp.write(f'✔ {line}')
            else:
                tmp.write(line)
    shutil.move(tmp.name, CHECKLIST_FILE)

def extract_quotes_from_markdown(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    md = MarkdownIt()
    tokens = md.parse(content)

    quotes = []
    for i in range(len(tokens)):
        if tokens[i].type == 'blockquote_open':
            # Find the next token that has type 'inline'
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
        print('Usage: python upload_quotes_to_readwise.py <folder_path>')
        sys.exit(1)

    folder_path = sys.argv[1]
    files_to_upload = scan_files(folder_path)
    update_checklist_file(files_to_upload)
    checklist = read_checklist_file()

    for file in files_to_upload:
        if f'✔ {file}' not in checklist:
            book_title = os.path.basename(os.path.dirname(file))
            quotes = extract_quotes_from_markdown(file)
            for quote in quotes:
                response = upload_quote_to_readwise(quote, book_title)
                print_upload_result(response, quote)
                if response.status_code == 201:
                    mark_uploaded_file(file)

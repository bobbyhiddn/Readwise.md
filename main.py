import os
import sys
import re
import shutil
import tempfile
from collections import Counter
from markdown_it import MarkdownIt
import requests

READWISE_API_KEY = 'MH27ZE7rlYwa2E4i8moa9zLTpIS9rcyQZukYVNnwsPBwKEW0mg'
READWISE_API_URL = 'https://readwise.io/api/v2/highlights/'
CHECKLIST_FILE = 'checklist.txt'

def extract_acronym(file_name):
    # Extract the part before the hyphen
    main_part = file_name.split('-')[0]
    
    # Split this part into words and extract the first letter from each word
    acronym = ''.join([part[0] for part in main_part.split() if part])
    
    return acronym

def scan_files(folder_path, acronym=None):
    folder_path = os.path.abspath(folder_path)
    files_to_upload = []
    print(f"Scanning folder: {folder_path}")
    acronyms = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if acronym is None:
                file_acronym = extract_acronym(file)
                acronyms.append(file_acronym)
            else:
                file_acronym = acronym
            if re.match(fr'{file_acronym}\s*-.*\.md', file, re.IGNORECASE):
                full_path = os.path.join(root, file)
                files_to_upload.append(full_path)
                print(f"Detected file: {full_path}")

    if acronym is None and acronyms:
        most_common_acronym = Counter(acronyms).most_common(1)[0][0]
        print(f"Using acronym: {most_common_acronym}")
        regex_pattern = fr'{most_common_acronym}.*\.md'
    else:
        print(f"Using provided acronym: {acronym}")
        regex_pattern = fr'{acronym}.*\.md'

    for root, _, files in os.walk(folder_path):
        for file in files:
            if re.match(regex_pattern, file, re.IGNORECASE):
                full_path = os.path.join(root, file)
                if full_path not in files_to_upload:
                    files_to_upload.append(full_path)
                    print(f"Detected file: {full_path}")

    return files_to_upload

def update_checklist_file(files_to_upload):
    if not os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE, 'w') as f:
            for file in files_to_upload:
                f.write(f'{file}\n')
                print(f"Added to checklist: {file}")

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
        print('Usage: python upload_quotes_to_readwise.py <folder_path> [acronym]')
        sys.exit(1)
    folder_path = sys.argv[1]
    acronym = sys.argv[2] if len(sys.argv) > 2 else None
    files_to_upload = scan_files(folder_path, acronym)
    print(f"Found {len(files_to_upload)} files to upload")
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
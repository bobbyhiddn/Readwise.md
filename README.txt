# Readwise Markdown Quote Uploader

This Python script uploads quotes extracted from markdown files to Readwise. It scans a specified folder for markdown files that match a given acronym or the most common acronym extracted from the filenames. The script then extracts quotes from the markdown files and uploads them to Readwise using the Readwise API.

## Requirements

- Python 3
- `markdown-it-py` package
- `requests` package

You can install the required packages using pip:

```bash
pip install markdown-it-py requests
```

## Usage

To use the script, run the following command:

```bash
python upload_quotes_to_readwise.py <folder_path> [acronym]
```

- `<folder_path>`: The path to the folder containing the markdown files.
- `[acronym]` (optional): The acronym to use for matching files. If not provided, the script will use the most common acronym extracted from the filenames.

Before running the script, make sure to set the `READWISE_API_KEY` environment variable to your Readwise API key. You can obtain your API key from the [Readwise API documentation](https://readwise.io/api_developer).

## Functions

The script contains the following functions:

- `extract_acronym(file_name)`: Extracts the acronym from a given filename.
- `scan_files(folder_path, acronym=None)`: Scans the specified folder for markdown files that match the given acronym or the most common acronym extracted from the filenames.
- `update_checklist_file(files_to_upload)`: Updates the checklist file with the list of files to upload.
- `read_checklist_file()`: Reads the checklist file and returns a list of lines.
- `mark_uploaded_file(file)`: Marks a file as uploaded in the checklist file.
- `extract_quotes_from_markdown(file_path)`: Extracts quotes from a markdown file.
- `upload_quote_to_readwise(quote, book_title)`: Uploads a quote to Readwise using the Readwise API.
- `print_upload_result(response, quote)`: Prints the result of the quote upload.

## Example

To upload quotes from markdown files in the folder "D:\Brain\Reading\Books\The Western Esoteric Traditions - Nicholas Goodrick-Clarke" with the acronym "TWET", run the following command:

```bash
python upload_quotes_to_readwise.py "D:\Brain\Reading\Books\The Western Esoteric Traditions - Nicholas Goodrick-Clarke" TWET
```

The script will scan the folder, extract quotes from the markdown files, and upload them to Readwise.
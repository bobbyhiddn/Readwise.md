# Readwise Markdown Uploader - Readwise.MD

The Readwise Markdown Uploader is a Python script that allows you to upload quotes from Markdown files to your Readwise account. You can organize your quotes into folders, and the script will extract the quotes from each Markdown file within the specified folder and upload them to Readwise.

### Prerequisites

- Python 3.6 or higher
- markdown-it-py library (install using pip install markdown-it-py)
- requests library (install using pip install requests)

```bash
pip install markdown-it-py requests
```

## Setup

Clone this repository or download the readwise_md.py script to your local machine.

Ensure you have obtained your Readwise API key. If you don't have one, you can get yours from the [Readwise website here](https://readwise.io/access_token).

Set your Readwise API key as an environment variable named READWISE_API_KEY. For example, on Linux or macOS:

```bash
Copy code
export READWISE_API_KEY=your_readwise_api_key_here
```

On Windows:

```powershell
setx READWISE_API_KEY "your_readwise_api_key_here"
```

## Usage

```bash
python readwise_md.py <folder_path> <prefix>
```

- <folder_path>: The path to the folder containing your Markdown files with quotes.
- <prefix>: (Optional) The common characters at the beginning of your quote files. If not provided, the script will use the folder name as the book title.

## Example
Suppose you have a folder structure like this:

```css
Copy code
└── Books
    ├── The Power of Music - Mannes
    │   ├── TPoM Pg.126 - A Song is Like a Crystal.md
    │   ├── TPoM Pg.144 - The Music of the Spheres.md
    │   └── ...
    ├── The Pattern On The Stone - Daniel Hillis
    │   └── TPotS - Pg. 127 - A Definitive Neural Network.md
    └── The Western Esoteric Traditions - Nicholas Goodrick-Clarke
    |   ├── TWET - Pg.42 - Some Quote.md
    |   ├── TWET - Pg.99 - Another Quote.md
    |
    └── Once Upon an Algorithm - Martin Erwing
        └── Pg. 42 - Recipes as Computation.md
    
```

To upload quotes from the folder "The Western Esoteric Traditions - Nicholas Goodrick-Clarke," you can run:

```bash
python readwise_md.py "D:\Brain\Reading\Books\The Western Esoteric Traditions - Nicholas Goodrick-Clarke" TWET
```

This will upload quotes from all the Markdown files within the specified folder and use "The Western Esoteric Traditions - Nicholas Goodrick-Clarke" as the book title.


In the example of Once Upon an Algorithm, you can see that I didn't use an acronym prefix for the Markdown file. If you use the consistent first two or three letters of a series of files, it will still work. For example, I had "Pg. as the prefix for all the Once Upon an Algorithm files. If I wanted to upload quotes from that book, I could run:

```bash
python readwise_md.py "D:\Brain\Reading\Books\Once Upon an Algorithm - Martin Erwing" Pg.
```

This will have the same effect as the previous command.

Please note that the script will handle UTF-8 encoded files, ensuring smooth processing of your Markdown files.

#### Troubleshooting

If you encounter any issues or have questions related to the script, feel free to ping me in discussions.

That's it! You can now easily upload your favorite quotes from Markdown files to Readwise using this simple Python script.

Happy reading and spellcrafting! 📚✨
# Progetto gestione dell'informazione

## Dependencies for the correct execution
```
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip3 install scrapetube

pip3 install whoosh
pip3 install torch --extra-index-url https://download.pytorch.org/whl/cpu
pip3 install scipy
pip3 install python-dateutil
```
> ℹ️ **_NOTE_**: The PyTorch dependency above is suited for a Linux system with no CUDA cores available. It may change from one device to another. See the official website: https://pytorch.org/get-started/locally/

## How to execute the application?

> ℹ️ **_NOTE_**: The Python version used in the project is 3.9.2. Running the app with another version of Python might cause unexpected behavior.

### On Linux or Mac
Launch the ```./main.sh``` file in the root directory of the project. The file containts a list available options that execute different Python files. They are listed as following:
1. Scrape - it scrapes all the data from the internet
2. Index - indexes the scraped documents
3. Benchmark - it runs all the benchmark queries which are in the **benchmarking/queries.txt** file and displays the results on the terminal
4. Search - it allows the user to enter a query and get the relative results
5. Run Flask App - runs a web server that allows the user to see the results on a GUI (website)

### On Windows
You must run each file (located in the root directory) individually, using the Command Prompt.

## Benchmarking

All the files needed for benchmarking can be found in the **benchmarking** directory of the project. It containes these items:
- **queries.txt** - contains UINs written in the query language
- **natural_language_queries.txt** - contains UINs written with natural language
- **queries_dcg** - directory that contains a list relevant documents for each query

The system is evaluated using the Discounted Cumulative Gain.
To execute the benchmark choose option 3 of the **main.sh** file or run the **execute_benchmark.py** file manually.
The results of the benchmark are shown on the terminal.

## Code documentation
All the Python files are documented using Google Docstrings. For more information on that refer to this link: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings

## Schema of a document
Documents in the **data** directory are in the JSON format. This is their schema:
> ℹ️ **_NOTE_**: The documents are encoded using UTF-8, however the actual characters in strings are backslash escaped (i.e. you won't be able to see emojis in the JSON files themselves). This does not affect the parsing of a document in Python
```json
{
    "video": {
        "id": "string",
        "publishedAt": "string (ISO 8601 format)",
        "title": "string",
        "description": "string",
        "duration": "string (ISO 8601 format)",
        "likes": "number",
        "views": "number"
    },
    "comments": [
        {
            "topLevelComment": "Comment",
            "replies": [
                "Comment"
            ]
        }
    ]
}
```
Here is the schema for a **Comment** element:
```json
{
    "id": "string",
    "publishedAt": "string (ISO 8601 format)",
    "author": "string",
    "text": "string",
    "likes": "number"
}
```

# Progetto gestione dell'informazione

## Dependencies for correct execution
```
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip3 install scrapetube

pip3 install whoosh
pip3 install torch --extra-index-url https://download.pytorch.org/whl/cpu
pip3 install scipy
pip3 install python-dateutil
pip3 install flask
```
> ℹ️ **_NOTE_**: The PyTorch dependency above is suited for a Linux system with no CUDA cores available. It may vary depending on your device. See the official website: https://pytorch.org/get-started/locally/

## How to execute the application

> ℹ️ **_NOTE_**: The Python version used in this project is 3.9. Running the app with a different version of Python might cause unexpected behavior.

### On Linux or Mac
Launch the `./main.sh` file in the root directory of the project. The file contains a list of available options that execute different Python files. They are listed as follows:
1. **Scrape** – Scrapes all data from the freeCodeCamp.org YouTube videos.
2. **Index** – Indexes the scraped documents.
3. **Benchmark** – Runs all the benchmark queries found in the **benchmarking/queries.txt** file and displays the results in the terminal.
4. **Search** – Allows the user to enter a query and get the corresponding results.
5. **Run Flask App** – Runs a web server that allows the user to view the results through a GUI (website).

### On Windows
You must run each file (located in the root directory) individually using the Command Prompt.

## Benchmarking

All files needed for benchmarking can be found in the **benchmarking** directory of the project. It contains the following items:
- **queries.txt** – Contains UINs written in the query language.
- **natural_language_queries.txt** – Contains UINs written in natural language.
- **queries_dcg** – A directory that contains lists of relevant documents for each query.

The system is evaluated using the Discounted Cumulative Gain (DCG) metric.

To execute the benchmark, choose option 3 in the **main.sh** file or run the **execute_benchmark.py** file manually.  
The benchmark results are displayed in the terminal.

## Code Documentation
All Python files are documented using Google-style docstrings. For more information, refer to this link: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings

## Document Schema
Documents in the **data** directory are in JSON format. This is their schema:
> ℹ️ **_NOTE_**: The documents are encoded using UTF-8. However, string characters are backslash-escaped (i.e., you won't be able to see emojis in the JSON files themselves). This does not affect the parsing of a document in Python.
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

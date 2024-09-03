# PO Chatbot
This project contains a basic web scraper that fetches and processes content from a website's main page and a few additional pieces of information. The goal is to extract content that can be used to answer simple questions based on the website's content.

## Files
**scraper.py:** The main scraper module that includes functions to fetch and process content from a website. It handles redirections and extracts the main content, as well as additional information like the page title, meta description, and internal links.

**chats.py:** A module for interacting with the OpenAI API. It sends the scraped content along with user questions to OpenAI and returns short answers.

**restAPI.py:** A FastAPI REST API that provides an endpoint to get processed content from a website and answer predefined questions.

**config_loader.py:** Loads configuration settings from a specified file (API key, model name, and port number)

## Setup
### Requirements
- `httpx`
- `BeautifulSoup4`
- `FastAPI`
- `uvicorn`

### Configuration
Create a configuration file at `.gitignore/config/config.txt` with the following format:
```
OPENAI_API_KEY=your_openai_api_key
MODEL_NAME=your_openai_model_name
PORT=your_port_number
```
And one at `.gitignore/config/questions.txt` containing the questions you want answered. 
For example:
```
What is the name?
What is the industry?
What is the company size?
What is the company's location?
What are the company's target markets?
```

### Usage
To start the REST API server, run the `restAPI.py` script. The server will be available at `http://0.0.0.0:8000` (or the port specified in your configuration):
```
python restAPI.py
```
The API provides an endpoint `/hostinfo/{host_name}` where you can retrieve information from a specified host.

Example usage:
`curl http://0.0.0.0:8000/hostinfo/example.com`
Or edit the URL on the local browser.

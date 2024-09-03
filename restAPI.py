# restAPI.py
# Description: FastAPI application that serves an endpoint that processes a website's main content 
#              and answers a set of predefined questions. The configuration settings are loaded 
#              from a file, and the app fetches the content of a specified host, then uses an 
#              asynchronous chat service to generate responses to the questions based on the content

from fastapi import FastAPI
from config_loader import load_config
import chats, scraper
from urllib.parse import urlparse

config = load_config("config/config.txt")

app = FastAPI()

# Function: load_questions
# Description: loads a list of questions from a specified text file. Each line in the file 
#              corresponds to one question. Empty lines ignored.
# Parameters:
#    - file_path (str): path to the text file containing the questions
# Returns:
#    - questions (list): a list of questions as strings
def load_questions(file_path: str) -> list:
    with open(file_path, 'r') as file:
        questions = [line.strip() for line in file if line.strip()]
    return questions


# Endpoint: /hostinfo/{host_name}
# Description: processes a given host URL to fetch its content and generates responses 
#              to predefined questions based on that content.
# Parameters:
#    - host_name (str): the host name or URL of the website to fetch
# Returns:
#    - responses (list): a list of responses generated for each question based on the website content
@app.get("/hostinfo/{host_name}", response_model=list)
async def get_host_info(host_name: str):
    if not host_name.startswith(('http://', 'https://')):
        host_name = 'https://' + host_name
    
    parsed_url = urlparse(host_name)
    full_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # fetchs the website content asynchronously
    website_content = scraper.scrape_website(full_url)
    
    # loads questions from the text file
    questions = load_questions("config/questions.txt")
    
    # processes each question asynchronously
    responses = [await chats.chat(website_content, question) for question in questions]
    
    return responses

if __name__ == "__main__":
    import uvicorn
    port = int(config.get("PORT", 8000))  # defaults to 8000 if not set
    uvicorn.run(app, host="0.0.0.0", port=port)
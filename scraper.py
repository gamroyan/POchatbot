# scraper.py
# Description: Fetches and processes the main content from a given website URL.
#              It can also retrieve additional pages linked from the main content page to enrich the
#              scraped data. The script uses asynchronous HTTP requests to fetch the content and parses
#              the HTML to extract relevant text while excluding irrelevant elements.

import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function: fetch_main_content
# Description: fetches and processes the main content of the given URL.
# Parameters:
#    - url (str): the URL of the website to scrape
# Returns:
#    - text (str): the cleaned and processed text content from the main page
def fetch_main_content(url):
    try:
        response = httpx.get(url, timeout=10.0, follow_redirects=True)  # follow_redirects=True to handle redirection
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # remove irrelevant elements
        for element in soup(["script", "style", "header", "footer", "nav", "aside", "form"]):
            element.decompose()

        # prefer main content areas
        main_content = soup.find("main") or soup.find("article") or soup.find("div", class_="content") or soup.body
        if main_content:
            text = main_content.get_text(separator="\n")
        else:
            text = soup.get_text(separator="\n")

        # clean up the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        print(f"Failed to fetch content from: {url}, Error: {e}")
        return ""


# Function: fetch_additional_info
# Description: fetches a few additional key pieces of information from the website
# Parameters:
#    - url (str): the URL of the website to scrape.
# Returns:
#    - info (dict): a dictionary containing the title, meta description, and any internal links
def fetch_additional_info(url):
    try:
        response = httpx.get(url, timeout=10.0, follow_redirects=True)  # follow_redirects=True to handle redirection
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.title.string if soup.title else "No title available"

        meta_description = soup.find("meta", attrs={"name": "description"})
        description = meta_description["content"] if meta_description else "No description available"

        # extract a few internal links
        internal_links = []
        for link in soup.find_all("a", href=True):
            full_url = urljoin(url, link["href"])
            if full_url.startswith(url):
                internal_links.append(full_url)
        
        return {
            "title": title,
            "description": description,
            "internal_links": internal_links[:5]  # limit to the first 5 internal links
        }
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        print(f"Failed to fetch additional info from: {url}, Error: {e}")
        return {}


# Function: scrape_website
# Description: combines the main content and additional info into a single result.
# Parameters:
#    - url (str): the URL of the website to scrape
# Returns:
#    - result (dict): a dictionary containing the main content and additional information
def scrape_website(url):
    main_content = fetch_main_content(url)
    additional_info = fetch_additional_info(url)
    
    result = {
        "main_content": main_content,
        "additional_info": additional_info
    }
    
    return result
from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup
from validate_url_helpers import *

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    if resp.status != 200:
        print(resp.error)
        return []
    
    # extract text from html
    try:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    except:
        return []
    links = []

    # check if page is valuable
    text = soup.get_text()
    words = text.split()
    if len(words) < 100:
        return []

    # find all links in the html
    for link in soup.find_all('a', href=True):
        # combine relative link to make absolute
        absolute = urljoin(url, link['href'])
        # defrag the link (as said in instructions)
        defragged, _ = urldefrag(absolute)
        links.append(defragged)

    return links

def is_valid(url):
    # Decide whether to crawl this url or not. 
    try:
        parsed = urlparse(url)
        if not validate_scheme(parsed): return False
        if not validate_domain(parsed): return False
        
        return base_validates(parsed)

    except TypeError:
        print ("TypeError for ", parsed)
        raise

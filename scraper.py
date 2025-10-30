from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup
from validate_url_helpers import *

def scraper(url, resp):
    print('Scraper Called')
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    if resp.status != 200:
        print(resp.error)
        return []
    
    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    links = []

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

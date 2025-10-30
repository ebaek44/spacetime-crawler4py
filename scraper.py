from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup
from validate_url_helpers import *
from validate_html_helpers import *
from report_helpers import *
from report_helpers import unique_urls


traps = set(['ics.uci.edu/~eppstein/pix','isg.ics.uci.edu/events'])


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    if resp.status != 200:
        print("Error:", resp.error)
        return []
    
    # extract text from html
    try:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    except:
        return []
    links = []
    text = soup.get_text()
    words = text.split()

    # create the report before checks
    unique_urls.add(url)
    highest_words(resp.url, words)

    if is_trap(resp.url, traps): return []
    if page_too_large(resp): return []
    if page_low_content(resp, soup, words): return []
    

    # find all links in the html
    for link in soup.find_all('a', href=True):
        absolute = urljoin(url, link['href']) # combine relative link to make absolute
        defragged, _ = urldefrag(absolute) # defrag the link (as said in instructions)
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

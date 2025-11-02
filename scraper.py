from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup
from validate_url_helpers import *
from validate_html_helpers import *
from report_helpers import *


traps = [
    "https://grape.ics.uci.edu/wiki/public/timeline?",
    "https://grape.ics.uci.edu/wiki/public/wiki",
    "https://grape.ics.uci.edu/wiki/asterix",
    "https://ics.uci.edu/events/category/student-experience/day",
    "https://grape.ics.uci.edu/wiki/public/zip-attachment",
    "https://isg.ics.uci.edu/wp-login.php",
    "http://mlphysics.ics.uci.edu/data",
    "https://ics.uci.edu/events/category/student-experience/list/?tribe-bar-date",
    "https://isg.ics.uci.edu/events",
    "https://grape.ics.uci.edu/wiki/public/raw-attachment"
    "https://www.ics.uci.edu/~eppstein",
    'calendar', 'login', 'ical', 'tribe', '/events', '/event', 'doku'
]


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    if resp.status != 200 or resp.raw_response == None:
        print("Error:", resp.error)
        return []
    
    # extract text from html
    try:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    except:
        return []
    links = []
    text = soup.get_text(separator=' ', strip=True)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()

    words = text.split() if text else []
    cleaned_words = clean_words(words)

    # create the report before checks
    unique_urls.add(url)
    report_highest_words(url, words)
    report_common_words(cleaned_words)
    report_uci_subdomain(url)


    if page_too_similar(words): return []
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

        if is_trap(url, traps): return False
        if not validate_scheme(parsed): return False
        if not validate_domain(parsed): return False
        
        return base_validates(parsed)

    except TypeError:
        print ("TypeError for ", parsed)
        raise


# english stop words set
STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 
    "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 
    'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 
    'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 
    'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', 
    "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", 
    "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 
    'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 
    'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', 
    "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 
    'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', 
    "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 
    'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 
    'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 
    'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 
    'your', 'yours', 'yourself', 'yourselves', "will", "can"
}


def clean_words(words):
    cleaned_words = []
    for word in words:
        # lowercase and clean
        clean_word = re.sub(r'[^a-z0-9]', '', word.lower())
        
        # skip if empty, is a stop word, or is a number
        if clean_word and clean_word not in STOP_WORDS and not clean_word.isdigit():
            if len(clean_word) > 1:
                cleaned_words.append(clean_word)
    return cleaned_words

import re
from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup

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
        # validate scheme
        if parsed.scheme not in set(["http", "https"]):
            return False

        # validate domain
        valid_domains = set([
            ".ics.uci.edu",
            ".cs.uci.edu", 
            ".informatics.uci.edu",
            ".stat.uci.edu"
        ])
        if not any(parsed.netloc.endswith(domain) for domain in valid_domains):
            return False

        print(parsed.netloc)


        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

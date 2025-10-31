from urllib.parse import urlparse
from collections import defaultdict

little_information = defaultdict(int)
THRESHOLD = 3  # block pattern after 3 low-info pages found

def page_low_content(resp, soup, words):
    if is_blocked_pattern(resp.url):
        return True
    
    # page not enough words
    if len(words) < 100 or len(str(soup)) < 500:
        add_little_information(resp)
        return True
    elif len(resp.raw_response.content) > 1_000_000:
        if len(words) < 500:
            add_little_information(resp)
            return True

    return False


def page_too_large(resp):
    content = resp.raw_response.content
    if len(content) > 10_000_000:
        return True

    return False


def is_blocked_pattern(url):
    pattern = get_pattern_from_url(url)
    return little_information[pattern] >= THRESHOLD


def add_little_information(resp):
    url = resp.url
    pattern = get_pattern_from_url(url)
    little_information[pattern] += 1


def get_pattern_from_url(url):
    # extract the directory pattern from url
    parsed = urlparse(url)
    parsed_path = parsed.path.split('/')
    
    if len(parsed_path) >= 3:
        url_parts = url.split('/')
        url_parts.pop()
        return '/'.join(url_parts)
    
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
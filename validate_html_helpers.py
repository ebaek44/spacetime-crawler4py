from urllib.parse import urlparse
from collections import defaultdict
import re
import hashlib

little_information = defaultdict(int)
seen_fingerprints = set()
THRESHOLD = 10  # block pattern after low-info pages found

def page_low_content(resp, soup, words):
    if is_blocked_pattern(resp.url):
        return True
    
    # page not enough words
    if len(words) < 50:
        add_little_information(resp)
        print('too small, less than 50 words')
        return True
    elif len(resp.raw_response.content) > MAX_FILE_SIZE_BYTES:
        if len(words) < 300:
            print('too large file and not enough words')
            add_little_information(resp)
            return True

    return False


def page_too_large(resp):
    content = resp.raw_response.content
    if len(content) > 2500000:
        print('file too big!')
        return True

    return False



# these functions are to process patterns in urls

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



# duplicate check code 

def make_ngrams(words):
    # 5 grams
    words = text.split()
    chunks = []
    for i in range(len(words) + 4):
        chunk = " ".join(words[i:i+size])
        chunks.append(chunk)
    return chunks

def randomize_ngrams(items):
    if len(items) <= 100:
        return items
    items = sorted(items, key=lambda x: hashlib.md5(x.encode()).hexdigest())
    return items[:100]

def hash_chunks(chunks):
    chosen = randomize_ngrams(chunks, 100)
    result = []
    for c in chosen:
        hashed = hashlib.sha256(c.encode()).hexdigest()
        result.append(hashed)
    return result

def check_similar(hashes):
    # THRESHOLD = 0.9, pretty leniant
    # true if dup
    if not hashes:
        return False
    similar = 0
    for h in hashes:
        if h in seen_fingerprints:
            similar += 1
    score = similar / len(hashes)
    return score > threshold

def add_all_hashes(hashes):
    for h in hashes:
        seen_fingerprints.add(h)

def page_too_similar(words):
    ngrams = make_ngrams(words)
    hashed = hash_chunks(ngrams)

    if not check_similar(hashed):
        add_hashes(hashed)
        # good
        return False

    else:
        return True
from urllib.parse import urlparse
from collections import defaultdict
import re
import hashlib

little_information = defaultdict(lambda: {'low': 0, 'total': 0})
seen_fingerprints = set()
MAX_BLOCKED_RATIO = 0.8  # block if 80% are low-content

def page_low_content(resp, soup, words):
    if is_blocked_pattern(resp.url):
        return True
    
    # page not enough words
    if len(words) < 50:
        add_little_information(resp, is_low=True)
        print('too small, less than 50 words')
        return True
    elif len(resp.raw_response.content) > 1_000_000:
        if len(words) < 300:
            print('too large file and not enough words')
            add_little_information(resp, is_low=True)
            return True

    add_little_information(resp, is_low=False)
    return False


def page_too_large(resp):
    content = resp.raw_response.content
    if len(content) > 2_500_000:
        print('file too big!')
        return True

    return False



# these functions are to process patterns in urls

def is_blocked_pattern(url):
    pattern = get_pattern_from_url(url)
    stats = little_information[pattern]

    # threshold is 50
    if stats['total'] < 50:
        return False
    
    # block if ration of low to total is too high
    ratio = stats['low'] / stats['total']
    return ratio >= MAX_BLOCKED_RATIO


def add_little_information(resp, is_low):
    url = resp.url
    pattern = get_pattern_from_url(url)
    little_information[pattern]['total'] += 1
    if is_low:
        little_information[pattern]['low'] += 1


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

def hash(text):
    result = 0
    for i, char in enumerate(text):
        result = result * 37 + ord(char)
        result = result % 1000000007
    return str(result).zfill(16)

def hash2(text):
    h = 5381 # prime long number
    for char in text:
        h = ((h * 33) + ord(char)) % (2**32)
    
    # make it look more random
    h = h ^ (h >> 16)
    h = h * 2654435761
    h = h % (2**32)
    
    return hex(h)[2:].zfill(16)

def make_ngrams(words):
    # 5 grams
    chunks = []
    for i in range(len(words) - 4):
        chunk = " ".join(words[i:i+5])
        chunks.append(chunk)
    return chunks

def randomize_ngrams(items):
    if len(items) <= 100:
        return items
    items = sorted(items, key=lambda x: hash(x))
    return items[:100]

def hash_chunks(chunks):
    chosen = randomize_ngrams(chunks)
    result = []
    for c in chosen:
        hashed = hash2(c)
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
    return score > 0.9

def add_all_hashes(hashes):
    for h in hashes:
        seen_fingerprints.add(h)

def page_too_similar(words):
    ngrams = make_ngrams(words)
    hashed = hash_chunks(ngrams)

    if not check_similar(hashed):
        add_all_hashes(hashed)
        # good
        return False

    else:
        return True
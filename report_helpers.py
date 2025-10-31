import time 
from urllib.parse import urlparse
from collections import Counter
import re

unique_urls = set()
highest_word = 0
highest_word_url = ""
uci_subdomains = {}

# TEST
repeated_paths = {}

# word freq tracking
word_frequencies = Counter()

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
    'your', 'yours', 'yourself', 'yourselves'
}

def process_words(words):
    # process and count word frequencies, filtering out stop words
    global word_frequencies
    
    for word in words:
        # convert word to lowercase
        clean_word = re.sub(r'[^a-z0-9]', '', word.lower())
        
        # skip if empty, is a stop word, or is a number
        if clean_word and clean_word not in STOP_WORDS and not clean_word.isdigit():
            # skip single characters
            if len(clean_word) > 1:
                word_frequencies[clean_word] += 1

def write_report():
    # write report at the end of the scrapers run
    with open('report.txt', 'w') as f:
        f.write(f"{str(int(time.time()))}\n")
        f.write(f"Unique pages found: {len(unique_urls)} \n")
        f.write(f"Highest words: {highest_word} from {highest_word_url}\n")
        
        # subdomains
        sorted_subdomains = sorted(list(uci_subdomains.items()), key=lambda x : x[0])
        subdomain_result = []
        for subdomain in sorted_subdomains:
            subdomain_result.append(subdomain[0])
            subdomain_result.append(subdomain[1])
        f.write(f"Subdomains sorted with frequency: {subdomain_result} \n")

        # TEST: repeated paths
        sorted_repeated_paths = sorted(list(repeated_paths.items()), key=lambda x : -x[1])
        f.write(f"TEST: Repeated Paths sorted with frequency: {sorted_repeated_paths} \n")
        f.write("\n")

        # write top 50 most common words
        f.write("="*60 + "\n")
        f.write("TOP 50 MOST COMMON WORDS (excluding stop words)\n")
        f.write("="*60 + "\n")
        
        top_50 = word_frequencies.most_common(50)
        for rank, (word, freq) in enumerate(top_50, 1):
            f.write(f"{rank}. {word}: {freq}\n")
        
        f.write("\n")
        f.write(f"Total unique words (excluding stop words): {len(word_frequencies)}\n")
        f.write("="*60 + "\n")


def report_highest_words(url, words):
    # always keep track of highest word count of html website
    global highest_word, highest_word_url
    if len(words) > highest_word:
        highest_word = len(words)
        highest_word_url = url
        print(highest_word)


def report_uci_subdomain(url):
    parsed = urlparse(url)
    domain = parsed.netloc.split('.')
    if len(domain) >= 2 and domain[-1] == 'edu' and domain[-2] == 'uci':
        # then it is a subdomain
        uci_subdomains[parsed.netloc] = uci_subdomains.get(parsed.netloc, 0) + 1

    
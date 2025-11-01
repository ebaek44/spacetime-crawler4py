from urllib.parse import urlparse
from collections import Counter
import re
from validate_html_helpers import little_information

unique_urls = set()
highest_word = 0
highest_word_url = ""
word_frequencies = Counter()
uci_subdomains = {}


def write_report():
    # write report at the end of the scrapers run
    with open('report.txt', 'w') as f:
        f.write(f"Unique pages found: {len(unique_urls)} \n \n \n")
        f.write(f"Highest words: {highest_word} from {highest_word_url}\n \n \n")
        
        # write top 50 most common words
        top_50 = word_frequencies.most_common(100)
        f.write(f"Highest 100 Words:\n")
        for rank, (word, freq) in enumerate(top_50, 1):
            f.write(f"{rank}. {word}: {freq}\n")

        # subdomains
        sorted_subdomains = sorted(list(uci_subdomains.items()), key=lambda x : -x[1])
        subdomain_result = []
        for subdomain in sorted_subdomains:
            subdomain_result.append((subdomain[0], subdomain[1]))
        f.write(f"\nSubdomains sorted with frequency: \n\n")
        for subdomain in subdomain_result:
            f.write(f"{subdomain[0]}: {subdomain[1]} \n")
            


def report_highest_words(url, words):
    # always keep track of highest word count of html website
    global highest_word, highest_word_url
    if words and len(words) > highest_word:
        highest_word = len(words)
        highest_word_url = url


def report_common_words(clean_words):
    # count word frequencies
    global word_frequencies
    for word in clean_words:
        word_frequencies[word] += 1


def report_uci_subdomain(url):
    parsed = urlparse(url)
    domain = parsed.netloc.split('.')
    if len(domain) > 2 and domain[-1] == 'edu' and domain[-2] == 'uci':
        # then it is a subdomain
        uci_subdomains[parsed.netloc] = uci_subdomains.get(parsed.netloc, 0) + 1

    
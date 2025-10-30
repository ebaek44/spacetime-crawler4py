import time 
from urllib.parse import urlparse

unique_urls = set()
highest_word = 0
highest_word_url = ""
uci_subdomains = {}

# TEST
repeated_paths = {}

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
        sorted_repeated_paths = sorted(list(repeated_paths.items()), key=lambda x : x[1])
        repeated_path_result = []
        for repeated_path in repeated_paths:
            repeated_path_result.append(repeated_path[0])
            repeated_path_result.append(repeated_path[1])
        f.write(f"TEST: Repeated Paths sorted with frequency: {repeated_path_result} \n")
        f.write("\n")


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

    
import re
from urllib.parse import urlparse

def is_trap(url, traps):
    # if a pattern of url keeps showing up over 100 times, its probably a trap.
    # interesting to find the number of what considers it a trap. 
    # need to run to see the numbers
    # do i do only the first path or second path too?

    if any(domain in url for domain in traps):
        return True

    return False


def validate_scheme(parsed):
    # validate scheme
    if parsed.scheme not in set(["http", "https"]):
        return False
    return True


def validate_domain(parsed):
    # validate domain
    valid_domains = set([
        ".ics.uci.edu",
        ".cs.uci.edu", 
        ".informatics.uci.edu",
        ".stat.uci.edu"
    ])
    if not any(parsed.netloc.endswith(domain) for domain in valid_domains):
        return False
    return True


def base_validates(parsed):
    # base check that we were given
    return not re.match(
        r".*\.(css|js|bmp|gif|jpe?g|ico"
        + r"|png|tiff?|mid|mp2|mp3|mp4"
        + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
        + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
        + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
        + r"|epub|dll|cnf|tgz|sha1"
        + r"|thmx|mso|arff|rtf|jar|csv"
        + r"|rm|smil|wmv|swf|wma|zip|rar|gz"
        + r"|mpg|py|h|cp|c|emacs|ppsx|lif|rle|nb|tsv|htm|odc|bib|pps|Z|ma)$", parsed.path.lower())


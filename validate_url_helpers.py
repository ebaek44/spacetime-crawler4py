import re
from urllib.parse import urlparse
from report_helpers import repeated_paths

def is_trap(url, traps):
    # if a pattern of url keeps showing up over 100 times, its probably a trap.
    # interesting to find the number of what considers it a trap. 
    # need to run to see the numbers
    # do i do only the first path or second path too?
    parsed = urlparse(url)


    # TEST
    path = parsed.path.split('/')
    path.pop(0)
    url_pattern = [parsed.netloc]
    for page in path:
        url_pattern.append(page)
    if len(url_pattern)>1:
        p = parsed.netloc + '/' + url_pattern[1]
        repeated_paths[p] = repeated_paths.get(p, 0) + 1
    if len(url_pattern)>2:
        p = parsed.netloc + '/' + url_pattern[1] + '/' + url_pattern[2]
        repeated_paths[p] = repeated_paths.get(p, 0) + 1
    # TEST, check if you are in trap
    if len(url_pattern)>1 and repeated_paths[p] > 300:
        return True

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
        + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())


def page_low_content(soup):
    text = soup.get_text()
    words = text.split()
    if len(words) < 100:
        return True
    if page_little_information(soup, words): 
        return True
    return False


def page_too_large(resp):
    content = resp.raw_response.content
    if len(content) > 5_000_000:
        return True
    return False


def page_little_information(soup, words):
    # too many repetitive words
    unique_words = set(words)
    if len(unique_words) < 50:
        return True
    
    # this compares text to html ratio
    html = str(soup)
    ratio = len(words) / len(html) if html_length > 0 else 0
    if ratio < 0.1:
        return True
    return False

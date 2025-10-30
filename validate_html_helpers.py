def page_low_content(soup):
    text = soup.get_text()
    words = text.split()
    if len(words) < 100:
        return True
    return False


def page_too_large(resp):
    content = resp.raw_response.content
    if len(content) > 5_000_000:
        return True
    return False
def page_valuable(soup):
    text = soup.get_text()
    words = text.split()
    if len(words) < 100:
        return False
    return True
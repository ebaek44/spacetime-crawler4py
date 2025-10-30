def page_low_content(resp, soup, words):
    # page not enough words
    if len(words) < 100 or len(str(soup)) < 500:
        return True
    elif len(resp.raw_response.content) > 1_000_000:
        if words < 500:
            return True

    return False


def page_too_large(resp):
    content = resp.raw_response.content
    if len(content) > 10_000_000:
        return True

    return False

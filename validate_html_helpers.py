def page_low_content(resp, soup, words):
    # IMPORTANT: page not enough words. maybe need to change the threshold?
    if len(words) < 50 or len(str(soup)) < 500:
        print('less than 50 words')
        return True
    elif len(resp.raw_response.content) > 1_000_000:
        if words < 500:
            print('less than 500 unique words')
            return True

    return False


def page_too_large(resp):
    content = resp.raw_response.content
    if len(content) > 10_000_000:
        print('too big')
        return True

    return False

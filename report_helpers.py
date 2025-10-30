import time 

unique_urls = set()
highest_word = 0
highest_word_url = ""

def write_report():
    with open('report.txt', 'w') as f:
        f.write(int(time.time()))
        f.write(f"Unique pages found: {len(unique_urls)}\n")
        f.write(f"Highest words: {highest_word} from {highest_word_url}\n")
        f.write("\n")


def highest_words(url, words):
    global highest_word, highest_word_url
    if len(words) > highest_word:
        highest_word = len(words)
        highest_word_url = url
        print(highest_word)
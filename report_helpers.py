import time 

unique_urls = set()

def write_report():
    with open('report.txt', 'w') as f:
        f.write(int(time.time()))
        f.write(f"Unique pages found: {len(unique_urls)}\n")
        f.write("\n")
        
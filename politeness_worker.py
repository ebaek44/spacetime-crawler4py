import time
from threading import Thread, Event, Lock
from urllib.parse import urlparse


POLITENESS_DELAY = 0.5 # 500 milleseconds

class PolitenessWorker(Thread):
    """
    This is the global worker for multithreading that will make sure the crawlers respect politeness and dont revisit the same url
    """
    def __init__(self, config):
        super().__init__(daemon=True)
        # This hash_map will track url: time
        self.polite_map = {}
        # This is a global visited set of urls
        self.visited = set()
        self.running = True
        self.lock = Lock()
        self.config = config

    # This will make the politeness worker stop running
    def stop(self):
        self.running = False

    # Workers will check to see if the url has already been visited
    def seen_url(self, url: str) -> bool:
        with self.lock:
            if url in self.visited:
                return False
            else:
                self.visited.add(url)
                return True
    
    def politeness_delay(self, url):
        domain = urlparse(url).netloc
        with self.lock:
            # grab the last visit
            last_visit = self.polite_map.get(domain, 0)
            now = time.time()
            diff = now - last_visit
            wait_time = self.config.time_delay - diff

            # If the domain hasnt been visited or its been more than 0.5 secs then its safe to crawl
            if wait_time <= 0:
                self.polite_map[domain] = now
                return
        # Else we will wait for the remaining politeness delay
        # Keep this outside the lock so other workers can call the function when the worker is sleeping
        time.sleep(wait_time)

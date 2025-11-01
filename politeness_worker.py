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
                return True
            self.visited.add(url)
            return False
    
    def politeness_delay(self, url):
        domain = urlparse(url).netloc
        with self.lock:
            last_visit = self.polite_map.get(domain, 0)
            now = time.time()
            diff = now - last_visit
            wait_time = self.config.time_delay - diff

            if wait_time <= 0:
                # Can visit immediately
                self.polite_map[domain] = now
                return
            
            # Reserve the next available slot for this domain
            # This prevents other threads from scheduling at the same time
            self.polite_map[domain] = last_visit + self.config.time_delay
        
        # Now sleep outside the lock - but the domain is already "reserved"
        time.sleep(wait_time)

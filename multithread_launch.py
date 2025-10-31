# import multiprocessing
import threading
import signal
from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler
from crawler.frontier import Frontier
from crawler.worker import Worker
from politeness_worker import PolitenessWorker

def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)

    # create the politeness worker to manage all 4 workers
    pw = PolitenessWorker(config)

    threads = []
    workers = min(config.threads_count, 4)
    # Name each worker seperatly and then 
    for i in range(workers):
        # each worker builds its own Frontier
        f = Frontier(config, restart, i)
        f.config.save_file = f"frontier_{i}.shelve"
        w = Worker(i, config, f, pw)
        w.start()
        threads.append(w)

    for w in threads: 
        w.join()

if __name__ == "__main__":    
    # so that i can cancel run and still print report 
    from report_helpers import write_report
    signal.signal(signal.SIGINT, lambda sig, frame: (write_report(), exit(0)))
    
    
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    main(args.config_file, args.restart, args.workers)

    # HOW TO RUN: python3 multithread_launch.py --workers 2
    # Change that 2 with any number for the amount of multithread workers you want


import os
import time
import methods
from napster_thread import napster_thread

os.chdir(os.path.dirname(os.path.realpath(__file__)))

class NapsterBot():
    
    def __init__(self, accounts_path, proxies_path, tracks_path):
        accounts = methods.load_accounts(accounts_path)
        proxies = methods.load_proxies(proxies_path)
        self.napster_threads = []
        self.message = ''
        if len(accounts) == len(proxies):
            self.credentials = dict(zip(accounts, proxies))
        else:
            self.message = 'You should have same number of accounts and proxies.'
            raise Exception(self.message)
        if len(self.credentials) != len(accounts):
            self.message = 'Duplicate sets of account:proxy were find.'
            raise Exception(self.message)
        self.thread_message = ''
        self.tracks = methods.load_tracks(tracks_path)
        self.threads = []
        self.logs = []
        self.stopped = False
        
    def get_nbthreads(self):
        return len(self.threads)
    
    def get_nbstreams(self):
        streams = 0
        for t in self.threads:
            streams += t.get_streams()
        return streams

    def check_threads(self):
        for t in self.threads:
            if t.is_stopped():
                self.threads.remove(t)

    def check_logs(self):
        new_logs = []
        for t in self.threads:
            new_logs.extend(t.get_logs())
        return new_logs
        
    def start_thread(self, cred, tracks):
        thread = napster_thread(cred, tracks)
        return thread

    def start(self):
        self.stopped = False
        self.threads = [ self.start_thread(cred, self.tracks) for cred in self.credentials.items() ]
        for t in self.threads:
            t.start()
            time.sleep(10)

    def stop(self):
        self.stopped = True
        for t in self.threads:
            t.stop()
        for t in self.threads:
            t.join()

    
import ctypes
import threading
from threading import Thread
from napster_user import User
from selenium.common.exceptions import TimeoutException

class napster_thread(Thread):
    
    def __init__(self, cred, tracks):
        Thread.__init__(self)
        self.cred = cred
        self.tracks = tracks
        self.user = ''
        self.stopped = False
        
    def run(self):
        self.stopped = False
        try:
            self.user = User(self.cred, self.tracks)
            try:
                while True:
                    if not self.user.displayed:
                        self.user.display()
                        self.user.displayed = True
                    if self.user.is_working():
                        self.user.stream()
                        self.user.displayed = False
                #self.user.test_ip() # we start the bot actions with the driver
            except TimeoutException: # if the page takes too long
                self.user.close_browser() # close the driver
                self.stopped = True
                raise # stop the thread by raising exception
            except: # if any other exception is raised
                self.user.close_browser() # close the driver
                self.stopped = True
                raise # stop the thread
        finally:
            print('Thread ended.')
            
    def is_stopped(self):
        return self.stopped

    def get_streams(self):
        if self.user:
            return self.user.get_streams()
        else:
            return 0

    def get_logs(self):
        if self.user:
            return self.user.get_logs()
        return []

    def get_id(self): 
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure')

    def stop(self):
        if self.user:
            self.user.close_browser()
        self.stopped = True
        self.raise_exception()
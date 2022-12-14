#/usr/bin/env python

import time

class Timer:

    def __init__(self):
        self.start_time = None

    def reset(self):
        self.start_time = time.time()

    def get_elapsed_time(self):
        return time.time() - self.start_time


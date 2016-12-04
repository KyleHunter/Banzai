from time import time


class Timer:

    start_time, total_ran, is_running = 0, 0, False

    def pause(self):
        if self.is_running:
            self.is_running = False
            self.total_ran += time() - self.start_time

    def reset(self):
        self.total_ran = 0
        self.start_time = self.total_ran
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time()

    def restart(self):
        self.reset()
        self.start()

    def elapsed_time(self):
        if self.is_running:
            return self.total_ran + time() - self.start_time
        else:
            return self.total_ran

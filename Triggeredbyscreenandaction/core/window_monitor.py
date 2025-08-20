import threading
import time

class WindowMonitor(threading.Thread):
    def __init__(self, trigger_manager):
        super().__init__()
        self.trigger_manager = trigger_manager
        self._stop_flag = threading.Event()
        self.daemon = True

    def run(self):
        while not self._stop_flag.is_set():
            self.trigger_manager.check_triggers()
            time.sleep(0.5)

    def stop(self):
        self._stop_flag.set()
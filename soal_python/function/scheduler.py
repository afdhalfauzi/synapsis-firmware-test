import time
import threading

class Scheduler:
    def __init__(self, func, interval=None) -> None:
        self.func = func
        self.interval = interval
        self._paused = threading.Event()
        self._stop = threading.Event()
        self._paused.clear()
        self.thread = threading.Thread(target=self._run)
            
    def start(self):
        if self.interval is None:
            self.interval =  self._prompt_interval()
        self.thread.start()
    
    def _run(self): 
        while not self._stop.is_set():
            if not self._paused.is_set():
                try:
                    self.func()
                except Exception as e:
                    print(f"[ERROR] error in sheduled function: {e}")
            time.sleep(self.interval)
            
    def pause(self):
        self._paused.set()
        print("[INFO] Scheduler paused")
    
    def resume(self):
        if self._paused.is_set():
            self._paused.clear()
            print("[INFO] Scheduler resumed")

    def stop(self):
        self._stop.set()
        self.thread.join()
        print("[INFO] Scheduler stopped")
        
    def _prompt_interval(self) -> int:
        while True:
            try:
                num = int(input("Enter scheduling interval time (sec): "))
                if num > 0:
                    print(f"[INFO] You entered: {num} second(s)")
                    return num
                else:
                    print("[WARN] Please enter number greater than 0.")
            except ValueError:
                print("[WARN] Invalid input. Please enter an integer")
    
    def set_interval(self, new_interval:int):
        if new_interval > 0:
            self.interval = new_interval
            print("[INFO] Interval sets to %d second(s)"%self.interval)
        else:
            print("[WARN] Please enter number greater than 0")

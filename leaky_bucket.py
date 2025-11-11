import time
import threading
from collections import deque

class LeakyBucket:
    def __init__(self, capacity: int, leak_rate_per_sec: float):
        self.capacity = capacity
        self.queue = deque()
        self.leak_rate = leak_rate_per_sec
        self.last = time.time()
        self.lock = threading.Lock()

    def _drain(self):
        now = time.time()
        elapsed = now - self.last
        to_drain = int(elapsed * self.leak_rate)
        for _ in range(to_drain):
            if self.queue:
                self.queue.popleft()
        if to_drain > 0:
            self.last = now

    def add(self, item) -> bool:
        with self.lock:
            self._drain()
            if len(self.queue) < self.capacity:
                self.queue.append(item)
                return True
            return False

if __name__ == "__main__":
    lb = LeakyBucket(capacity=3, leak_rate_per_sec=0.5)  # capacity 3, leak 0.5 req/sec
    print("LeakyBucket: capacity=3, leak=0.5/sec - try 10 requests (0.6s apart)")
    for i in range(10):
        ok = lb.add(f"req_{i+1}")
        print(f"{i+1:02d}: {'enqueued' if ok else 'dropped'} (queue={len(lb.queue)})")
        time.sleep(0.6)
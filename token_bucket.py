import time
import threading

class TokenBucket:
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.refill_rate = float(refill_rate_per_sec)
        self.last = time.time()
        self.lock = threading.Lock()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last
        if elapsed > 0:
            add = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + add)
            self.last = now

    def consume(self, tokens: float = 1.0) -> bool:
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

if __name__ == "__main__":
    tb = TokenBucket(capacity=5, refill_rate_per_sec=1.0)
    print("TokenBucket: capacity=5, refill=1/sec - try 12 requests (0.6s apart)")
    for i in range(12):
        ok = tb.consume()
        print(f"{i+1:02d}: allowed={ok}, tokens_left={tb.tokens:.2f}")
        time.sleep(0.6)
import asyncio
import time


class TokenBucket:
    # classic token bucket, tokens refill over time and each request takes one

    def __init__(self, rate, capacity):
        self.rate = rate  # tokens per second
        self.capacity = capacity
        self.tokens = capacity  # start full
        self.last = time.monotonic()
        self.lock = asyncio.Lock()

    async def acquire(self):
        # take one token, wait untill one is available
        while True:
            async with self.lock:
                now = time.monotonic()
                # refill based on how much time passed
                self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
                self.last = now
                if self.tokens >= 1:
                    self.tokens -= 1
                    return
            # bucket empty, sleep a tiny bit and try again
            await asyncio.sleep(1 / self.rate)

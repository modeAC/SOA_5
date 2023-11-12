import time


class PerClientLimiter:
    def __init__(self, default_limit: int = 5, update_every: int = 60):
        self.client2limit: dict = {}
        self.client2req_count: dict = {}
        self.client2last_updated: dict = {}
        self.update_every = update_every

    def __call__(self, client: str):
        if client in self.client2limit:
            cur_time = time.time()
            if cur_time > self.client2last_updated[client] + self.update_every:
                self.client2req_count[client] = 0
                self.client2last_updated[client] = cur_time
            self.client2req_count[client] += 1
            return self.client2limit[client] >= self.client2req_count[client]
        return False

    def register_client(self, client: str, limit: int):
        self.client2limit[client] = limit
        self.client2req_count[client] = 0
        self.client2last_updated[client] = time.time()


class GeneralLimiter:
    def __init__(self, default_limit: int = 5, update_every: int = 60):
        self.limit = default_limit
        self.req_count = 0
        self.last_updated = time.time()
        self.update_every = update_every

    def __call__(self, client: str):
        cur_time = time.time()
        if cur_time > self.last_updated + self.update_every:
            self.req_count = 0
            self.last_updated = cur_time
        self.req_count += 1
        return self.limit >= self.req_count

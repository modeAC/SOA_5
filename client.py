import datetime
import threading
import time

import requests

from python.rate_limiter.utils import GeneralLimiter


class Client:
    def __init__(self, url: str, user_id: str, limit: int = 4, update_every: int = 60):
        self.url = url
        self.user_id = user_id
        self.limiter = GeneralLimiter(default_limit=limit, update_every=update_every)
        self.allow_input = True
        self.__q = []
        self.__t = threading.Thread(target=self.process_q)
        self.__t.start()

    def run(self):
        k = ''
        while k != 'close':
            if self.allow_input:
                k = input('Send request (yes/no/close): ')
                if k.lower() == 'yes':
                    self.__q.append({'client': self.user_id})
                    self.allow_input = False
            time.sleep(1)

    def process_q(self):
        while True:
            if len(self.__q) > 0:
                if self.limiter(self.user_id):
                    response = requests.get(self.url, json=self.__q.pop())
                    print(f'{datetime.datetime.now().strftime("%H:%M:%S")}', response.text+'\n' if response.ok else None, response.status_code)
                else:
                    print('Reached per minute limit. Request added to the queue.')
                    time.sleep(5)
            else:
                self.allow_input = True


if __name__ == '__main__':
    url = 'http://192.168.49.2:30001'
    user_id = 'user_1'
    limit = 4
    update_every = 60

    c = Client(url, user_id, limit, update_every)
    c.run()

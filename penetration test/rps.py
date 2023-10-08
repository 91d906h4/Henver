# Send n requests persecond to Henver.
# 
# The max RPS (Requests Per Second) of Henver HTTP Server is about 1000 
# with Intel Code i7 CPU.

import threading
import requests

def test():
    for _ in range(100):
        requests.request("GET", "http://127.0.0.1/temp/test.php?test=222")

for _ in range(1000):
    threading.Thread(target=test).start()

print("done")
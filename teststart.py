# unicoding: utf-8
import requests
import threading as tr

import www
import time


def cb():
    time.sleep(5)
    req = requests.get("http://localhost:5000/main/sc/init")


app = www.create_app()
if __name__ == "__main__":
    tr1 = tr.Thread(target=cb)
    tr1.start()
    app.run(host="0.0.0.0", port=5000)

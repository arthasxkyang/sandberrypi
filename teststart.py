# unicoding: utf-8
import requests
import threading as tr

import www
import time


def cb():
    # 此处项目经理要求延迟两秒XD
    time.sleep(2)
    req = requests.get("http://localhost:5000/main/sc/init")


app = www.create_app()
if __name__ == "__main__":
    tr1 = tr.Thread(target=cb)
    # tr1.start()
    app.run(host="0.0.0.0", port=5000)

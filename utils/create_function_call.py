import json
import logging
import re

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

logging.root.setLevel(logging.INFO)

PROXY_PORT = "63372"
CREATE = True

config = {
    "runtime": "PYTHON",
    "inputs": ["persistent://public/functions/inTopic"],
    "output": "persistent://public/functions/outTopic",
    "className": "simple_addition_function.AdditionFunction",
    "py": "simple_addition_function.py"
}


def gen_encoder():
    return MultipartEncoder(fields={"functionConfig": (None, json.dumps(config), 'application/json'),
                                    "data": ("simple_addition_function.py",
                                             open('simple_addition_function.py', 'rb'),
                                             'text/plain')})


def request_args():
    encoder = gen_encoder()
    return {
        "url": f"http://localhost:{PROXY_PORT}/admin/v3/functions/public/functions/myFunction",
        "data": encoder,
        "headers": {'Content-Type': encoder.content_type}
    }


res = requests.put(**request_args())

if res.status_code == 400 and len(re.findall("Function .* doesn't exist", res.text)) > 0:
    res = requests.post(**request_args())


logging.info(f"Response ({res.status_code}): {res.text}")

if __name__ == '__main__':
    pass

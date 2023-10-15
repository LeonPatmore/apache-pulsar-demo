import json
import logging

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

logging.root.setLevel(logging.INFO)

config = {
    "runtime": "PYTHON",
    "inputs": ["functionIn"],
    "output": "functionOut",
    "className": "simple_addition_function.AdditionFunction",
    "py": "simple_addition_function.py"
}

encoder = MultipartEncoder(fields={"functionConfig": (None, json.dumps(config), 'application/json'),
                                   "data": ("simple_addition_function.py",
                                            open('simple_addition_function.py', 'rb'),
                                            'text/plain')})

res = requests.put('http://localhost:52498/admin/v3/functions/public/functions/myFunction',
                   data=encoder,
                   headers={'Content-Type': encoder.content_type})

logging.info(f"Response ({res.status_code}): {res.text}")

if __name__ == '__main__':
    pass

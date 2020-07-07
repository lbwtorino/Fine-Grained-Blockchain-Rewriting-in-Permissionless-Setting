import requests
import random
import json

response = requests.post(f'http://127.0.0.1:8001/register_node', json={"node_address": "http://127.0.0.1:8002"})
print(response)


response1 = requests.get('http://127.0.0.1:8002/chain')
print(response1)
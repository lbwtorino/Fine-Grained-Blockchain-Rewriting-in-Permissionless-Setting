import datetime
import json
from hashlib import sha256


import requests
from flask import render_template, redirect, request

from app import app
from merkle import hashfunc

# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []


def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/')
def index():
    # fetch_posts()
    return render_template('index.html',
                           title='Decentralized nodes',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    post_content = request.form["content"]
    author = request.form["author"]

    # tx_hash = sha256(str(post_content).encode()).hexdigest()
    to_modify_content = str(hashfunc(post_content))
    # tx_hash = sha256(str(to_modify_content).encode()).hexdigest()
    tx_hash = sha256(to_modify_content.encode()).hexdigest()
    # print(hashlib.sha256(str(hash_text['b']).encode()).hexdigest())

    post_object = {
        'author': author,
        'content': post_content,
        'to_modify': to_modify_content,
        'tx_hash': tx_hash
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')

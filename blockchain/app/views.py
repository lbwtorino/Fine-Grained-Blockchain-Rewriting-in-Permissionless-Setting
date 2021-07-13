import datetime
import json
from hashlib import sha256


import requests
from flask import render_template, redirect, request

from app import app
from merkle import hashfunc

# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8001"

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
    res = hashfunc(int(post_content))
    # b, verify_text, adapt_text['message_prime'], adapt_text['p_prime'], adapt_text['b'], adapt_text['random_r_prime'], adapt_text['C_prime'], adapt_text['c_prime'], adapt_text['epk_prime'], adapt_text['sigma_prime'], adapt_text['res_prime']
    chameleon_hashvalue = str(res[0])
    oldhash_verify, message_prime, p_prime, b_prime, random_r_prime, C_prime, c_prime, epk_prime, sigma_prime, newhash_verify = str(res[1]), str(res[2]), str(res[3]), str(res[4]), str(res[5]), str(res[6]), str(res[7]), str(res[8]), str(res[9]), str(res[10])
    # message = str(hashfunc(int(post_content))[1])
    # tx_hash = sha256(to_modify_content.encode()).hexdigest()
    tx_hash = str(res[0])
    # print(hashlib.sha256(str(hash_text['b']).encode()).hexdigest())
    output = {'tx_hash': tx_hash, 'old content': post_content, 'chameleon_hashvalue': chameleon_hashvalue, 'oldhash_verify': oldhash_verify, 'message_prime': message_prime, 'p_prime': p_prime, 'newchameleon_hashvalue': b_prime,'random_r_prime': random_r_prime, 'C_prime': C_prime, 'c_prime': c_prime, 'epk_prime': epk_prime, 'sigma_prime': sigma_prime,'newhash_verify': newhash_verify}
    with open('./rewrite_data/' + str(tx_hash) + '.txt', 'w') as file:
        file.write(json.dumps(output))

    post_object = {
        'author': author,
        'content': post_content,
        # 'chameleon_hashvalue': chameleon_hashvalue,
        'tx_hash': chameleon_hashvalue
    }


    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')

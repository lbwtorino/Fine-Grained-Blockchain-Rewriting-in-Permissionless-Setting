import string
import hashlib
from merklelib import MerkleTree, beautify, export
from hashlib import sha256
import charm.core.crypto.cryptobase
from charm.toolbox.pairinggroup import *
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import *
from chameleon import CHAMELEON
import argparse
import random

curve = 'MNT224'
groupObj = PairingGroup(curve)
chameleon = CHAMELEON(groupObj)
(mpk, msk) = chameleon.setup()

def hashfunc(value):
#   return hashlib.sha256(str(value).encode()).hexdigest()
    return chameleon.generate_chameleon_hash(mpk, value)['b']

def defaulthash(value):
    return hashlib.sha256(value).hexdigest()


# a list of all ASCII letters
# data = list(string.ascii_letters)
# data = ['1', '2']

# build a Merkle tree for that list
# tree = MerkleTree(data, hashfunc)
# print(tree)
# beautify(tree)
# print(ttt)
# export(tree, filename='transactions')
# st = str('2793603d2dbc9ecb01075e8ee79c9705840bfde2d7e04ddfc952aea2ae46e79c') + str('6ee8afcc0c19ab6c4193a332f862a85931093e425e417a598e9586c118fbcd47')
# a = 1
# test = b'\x00' + '1'.encode()
# test = '1'.encode()
# print(test)
# test = 1
# print(hashlib.sha256(str(test).encode()).hexdigest())

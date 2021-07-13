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
policy = '(123 or 444) and (231 or 384)'
sk = chameleon.keygen(mpk, msk, policy)

def hashfunc(value):
#   return hashlib.sha256(str(value).encode()).hexdigest()
    # res = chameleon.generate_chameleon_hash(mpk, value)
    # b = res['b']
    # return chameleon.generate_chameleon_hash(mpk, value)['b']
    message = groupObj.init(ZR, int(value))
    attri_list = {'123', '444',  '231', '384'}
    hash_text = chameleon.hash(mpk, msk, message, attri_list)
    p_prime, b, random_r = hash_text['p_prime'], hash_text['b'], hash_text['random_r']
    C, c, epk, sigma = hash_text['C'], hash_text['c'], hash_text['epk'], hash_text['sigma']
    keypair_pk = hash_text['keypair_pk']
    verify_text = chameleon.verify(mpk, message, p_prime, b, random_r, C, c, epk, sigma, keypair_pk)
    # m′, p′, b, r′, C′, c′, epk′, σ′
    # return {'message_prime':message_prime, 'p_prime':p_prime, 'b':b, 'random_r_prime':random_r_prime, 'C_prime':C_prime, 'c_prime':c_prime, 'epk_prime': epk_prime, 'sigma_prime': sigma_prime, 'res_prime':res_prime}
    adapt_text = chameleon.adapt(mpk, msk, sk, message, p_prime, b, random_r, C, c, epk, sigma, keypair_pk)
    return b, verify_text, adapt_text['message_prime'], adapt_text['p_prime'], adapt_text['b'], adapt_text['random_r_prime'], adapt_text['C_prime'], adapt_text['c_prime'], adapt_text['epk_prime'], adapt_text['sigma_prime'], adapt_text['res_prime']

def defaulthash(value):
    return hashlib.sha256(value).hexdigest()

print(groupObj.init(ZR, int(100)))


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

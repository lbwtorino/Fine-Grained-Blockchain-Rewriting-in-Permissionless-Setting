import charm.core.crypto.cryptobase
import hashlib
from charm.toolbox.pairinggroup import *
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import *
from chameleon import CHAMELEON
import argparse
import random
import time
from hashlib import sha256


def main():

    curve = 'MNT224'
    groupObj = PairingGroup(curve)
    chameleon = CHAMELEON(groupObj)

    (mpk, msk) = chameleon.setup()


    policy = '(123 or 444) and (231 or 384)'
    sk = chameleon.keygen(mpk, msk, policy)

    # message = groupObj.random(ZR)
    i = 1
    message = groupObj.init(ZR, int(1))
    attri_list = {'123', '444',  '231', '384'}
    hash_text = chameleon.hash(mpk, msk, message, attri_list)
    print(hash_text['message'])
    print(hash_text['b'])
    print(type(hash_text['b']))
    print(hashlib.sha256(str(hash_text['b']).encode()).hexdigest())


    p_prime, b, random_r = hash_text['p_prime'], hash_text['b'], hash_text['random_r']
    C, c, epk, sigma = hash_text['C'], hash_text['c'], hash_text['epk'], hash_text['sigma']
    keypair_pk = hash_text['keypair_pk']
    verify_text = chameleon.verify(mpk, message, p_prime, b, random_r, C, c, epk, sigma, keypair_pk)

    adapt_text = chameleon.adapt(mpk, msk, sk, message, p_prime, b, random_r, C, c, epk, sigma, keypair_pk)
    print(adapt_text['message_prime'])
    print(adapt_text['b'])

if __name__ == "__main__":
    debug = True
    main()
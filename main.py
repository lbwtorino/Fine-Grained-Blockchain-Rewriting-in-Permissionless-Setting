import charm.core.crypto.cryptobase
from charm.toolbox.pairinggroup import *
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import *
from scheme import SCHEME
from sharing import SHARING
import argparse
import random
import time
from hashlib import sha256




def main():

    # post_content = str(123)
    # print(sha256(post_content.encode()).hexdigest())

    curve = 'MNT224'
    groupObj = PairingGroup(curve)
    scheme = SCHEME(groupObj)

    (mpk, msk) = scheme.setup()

    parser = argparse.ArgumentParser()
    parser.add_argument("modules")
    args = parser.parse_args()

    if args.modules == 'ABET':
        policy = '(123 or 444) and (231 or 384)'
        sk = scheme.keygen(mpk, msk, policy)

        message = groupObj.random(ZR)
        attri_list = {'123', '444',  '231', '384'}
        hash_text = scheme.hash(mpk, msk, message, attri_list)


        p_prime, b, random_r = hash_text['p_prime'], hash_text['b'], hash_text['random_r']
        C, c, epk, sigma = hash_text['C'], hash_text['c'], hash_text['epk'], hash_text['sigma']
        keypair_pk = hash_text['keypair_pk']
        print("\n\n\n================================Verify()======================================")
        verify_text = scheme.verify(mpk, message, p_prime, b, random_r, C, c, epk, sigma, keypair_pk)

        adapt_text = scheme.adapt(mpk, msk, sk, message, p_prime, b, random_r, C, c, epk, sigma, keypair_pk)

    elif args.modules == 'DPSS':
        # print(time.time())
        share = SHARING(groupObj)
        alpha = msk['alpha']
        S = groupObj.init(ZR, int(alpha))
        print("\n\n=============================== Secret (i.e., msk['alpha']) ======================================")
        print("\n\nSecret:\n", S)

        threshold = 2
        n = 2 * threshold + 1
        shares_A = share.get_GroupA_shares(S, threshold)
        print("\n\n=============================== Distribute shares to Committee A ======================================")
        print("\n\nThe shares to Committee A:\n", shares_A)
        
        # A1 = [B1, B2, B3, B4, B5], A2 = [B1, B2, B3, B4, B5].......
        reshare_A = []
        for i in shares_A:
            # share.reshare_GroupA_shares(i) contains 5 numbers/points
            reshare_A.append(share.reshare_GroupA_shares(i))
        print("\n\n=============================== Re-calculate shares in Committee A ======================================")
        print("==================== Distribute new shares from Committee A to Committee B ==============================")
        print("\n\nThe shares from Committee A to Committee B:\n", reshare_A)


        # shares_B is a size_A * size_B list, shares_B[i] has 5 numbers/points
        shares_B = share.get_GroupB_shares(reshare_A)
        print("\n\n=============================== Committee B members receive share slices from Committee A ======================================")
        print("===========================================Committee B members recover new shares ==============================================")
        print("\n\nThe new shares in Committee B:\n", shares_B)

        # return coefficient [0, a1, a2,.....an]
        new_polynomial = share.generate_new_polynomial()

        B = [None] * (n)
        for i in range(n):
            # recover_secret() reutn {'constant': xx, 'x^1':xx, 'x^2':xx,......'x^n':xx}
            B[i] = share.update_polynomial(share.recover_secret(shares_B[i]), new_polynomial)

        updated_S = share.update(B)
        # print(time.time())
        print("\n\n=============================== Recovered Secret in Committee B ======================================")
        print("recovered_Secret:\n", share.recover_secret(updated_S))

    else:
        print("Invalid argument.")

if __name__ == "__main__":
    debug = True
    main()

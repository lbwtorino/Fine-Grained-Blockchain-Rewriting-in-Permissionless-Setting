import charm.core.crypto.cryptobase
from charm.toolbox.pairinggroup import *
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import *
# from charm.toolbox.pairinggroup import PairingGroup, GT
# from kpabe import KPABE
# from ibe import KPIBE
from scheme import SCHEME
from sharing import SHARING
import argparse
import random
import time



def main():

    curve = 'MNT224'
    groupObj = PairingGroup(curve)
    scheme = SCHEME(groupObj)

    (mpk, msk) = scheme.setup()

    policy = '(123 or 444) and (231 or 384)'
    start_time = time.time()
    # ttt = []
    # for i in range(100):
    #     print(i, mpk, msk)
    #     ttt.append(scheme.keygen(mpk. msk, policy))
    # end_time = time.time()
    # print(start_time, end_time, end_time - start_time)
    
    sk = scheme.keygen(mpk, msk, policy)
    end_time = time.time()
    print(start_time, end_time, end_time - start_time)

    parser = argparse.ArgumentParser()
    parser.add_argument("modules")
    args = parser.parse_args()

    if args.modules == 'ABET':
        message = groupObj.random(ZR)
        attri_list = {'123', '444',  '231', '384'}
        # ct = scheme.encrypt(mpk, msk, message, attri_list)
        start_time1 = time.time()
        hash_text = scheme.hash(mpk, msk, message, attri_list)
        end_time1 = time.time()
        # print(start_time1, end_time1, end_time1 - start_time1)


        p_prime, b, random_r = hash_text['p_prime'], hash_text['b'], hash_text['random_r']
        C, c, epk, sigma = hash_text['C'], hash_text['c'], hash_text['epk'], hash_text['sigma']
        keypair_pk = hash_text['keypair_pk']
        start_time2 = time.time()
        verify_text = scheme.verify(mpk, message, p_prime, b, random_r, C, c, epk, sigma, keypair_pk)
        end_time2 = time.time()
        # print(start_time2, end_time2, end_time2 - start_time2)

        print(verify_text)

        start_time3 = time.time()
        adapt_text = scheme.adapt(mpk, msk, sk, C, message, p_prime, b, random_r, C, c, epk, sigma, keypair_pk)
        end_time3 = time.time()
        print(start_time3, end_time3, end_time3 - start_time3)

    elif args.modules == 'DPSS':
        share = SHARING(groupObj)
        alpha = msk['alpha']
        S = groupObj.init(ZR, int(alpha))
        print("S:")
        print(S)

        shares_A = share.get_GroupA_shares(S)
        print("shares_A:")
        print(shares_A)
        

        # A1 = [B1, B2, B3, B4, B5], A2 = [B1, B2, B3, B4, B5].......
        reshare_A = []
        for i in shares_A:
            # share.reshare_GroupA_shares(i) contains 5 numbers/points
            reshare_A.append(share.reshare_GroupA_shares(i))
        print("reshare_A:")
        print(reshare_A)


        # shares_B is a size_A * size_B list, shares_B[i] has 5 numbers/points
        shares_B = share.get_GroupB_shares(reshare_A)
        print("shares_B:")
        print(shares_B)

        constant_prime, a1_prime, a2_prime = 0, groupObj.init(ZR, int(random.randrange(1000))), groupObj.init(ZR, int(random.randrange(1000)))
        B1 = share.update_polynomial(share.recover_secret(shares_B[0]), constant_prime, a1_prime, a2_prime)
        B2 = share.update_polynomial(share.recover_secret(shares_B[1]), constant_prime, a1_prime, a2_prime)
        B3 = share.update_polynomial(share.recover_secret(shares_B[2]), constant_prime, a1_prime, a2_prime)
        B4 = share.update_polynomial(share.recover_secret(shares_B[3]), constant_prime, a1_prime, a2_prime)
        B5 = share.update_polynomial(share.recover_secret(shares_B[4]), constant_prime, a1_prime, a2_prime)

        B = [B1, B2, B3, B4, B5]

        updated_S = share.update(B)
        print("recovered_S:")
        print(share.recover_secret(updated_S))


        

    else:
        print("Invalid argument.")

if __name__ == "__main__":
    debug = True
    main()
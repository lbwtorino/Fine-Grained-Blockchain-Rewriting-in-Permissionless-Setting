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


def main():

    curve = 'MNT224'
    groupObj = PairingGroup(curve)
    scheme = SCHEME(groupObj)

    (mpk, msk) = scheme.setup()

    policy = '(123 or 444) and (231 or 999)'	
    sk = scheme.keygen(mpk, msk, policy)

    parser = argparse.ArgumentParser()
    parser.add_argument("modules")
    args = parser.parse_args()

    if args.modules == 'ABET':
        message = groupObj.random(ZR)
        attri_list = {'123', '842',  '231', '384'}
        # ct = scheme.encrypt(mpk, msk, message, attri_list)
        hash_text = scheme.hash(mpk, msk, message, attri_list)

        p_prime, b, random_r = hash_text['p_prime'], hash_text['b'], hash_text['random_r']
        C, c, epk, sigma = hash_text['C'], hash_text['c'], hash_text['epk'], hash_text['sigma']
        keypair_pk = hash_text['keypair_pk']
        verify_text = scheme.verify(mpk, message, p_prime, b, random_r, C, c, epk, sigma, keypair_pk)
        print(verify_text)

        adapt_text = scheme.adapt(mpk, msk, sk, C, message, p_prime, b, random_r, C, c, epk, sigma, keypair_pk)
    elif args.modules == 'DPSS':
        share = SHARING(groupObj)
        alpha = msk['alpha']
        S = groupObj.init(ZR, int(alpha))
        print("S:\n")
        print(S)

        shares_A = share.get_GroupA_shares(S)
        print("shares_A:\n")
        print(shares_A)
        test = []
        for i in range(5):
            test.append(shares_A[i][0])
        print(share.recover_secret(test))
        
        reshare_A = []
        for i in shares_A:
            # share.reshare_GroupA_shares(i) contains 5 numbers/points
            reshare_A.append(share.reshare_GroupA_shares(i))
        print("reshare_A:\n")
        print(reshare_A)

        # shares_B is a size_A * size_B list, shares_B[i] has 5 numbers/points
        shares_B = share.get_GroupB_shares(reshare_A)
        print("shares_B:\n")
        print(shares_B)
        recovered_S = []
        for i in shares_B:
            # recovered_S.append(share.recover_secret(i))
            res = share.recover_secret(i)
            print(res)
            recovered_S.append(res['constant'])
        
        print(share.recover_secret(recovered_S))


    else:
        print("Invalid argument.")

if __name__ == "__main__":
    debug = True
    main()
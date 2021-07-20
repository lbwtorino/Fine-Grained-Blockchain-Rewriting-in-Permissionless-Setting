import charm.core.crypto.cryptobase
from charm.toolbox.pairinggroup import *
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import *
from fractions import Fraction
import random
import numpy as np

class SHARING(ABEnc):
    def __init__(self, groupObj, verbose = False):
        ABEnc.__init__(self)
        global util, group
        group = groupObj
        util = SecretUtil(group, verbose)
        self.size_A = 5
        self.size_B = 5
        self.threshold = 2

    def compute_polynomial(self, share, x):
        # return constant + a1 * x + a2 * (x**2)
        res = 0
        for i in range(len(share)):
            res += share[i] * x**(i)
        return res
    
    def compute_polynomial_xy(self, S, coefficient, x):
        # x is set to a particular "value"
        res = [None] * (self.threshold+1)
        constant = S
        for i in range(self.threshold):
            constant += coefficient[3*i] * x**(i+1)
        res[0] = constant
        for i in range(1, self.threshold+1):
            res[i] = coefficient[3*(i-1)+1] + coefficient[3*(i-1)+2] * x**(i)
        return res


    def get_GroupA_shares(self, S, threshold):
        self.threshold = threshold
        self.size_A, self.size_B = 2 * threshold + 1, 2 * threshold + 1
        coefficient = []
        for i in range(3*self.threshold):
            coefficient.append(group.init(ZR, int(random.randrange(1000))))
        shares = []
        for i in range(self.size_A):
            shares.append(self.compute_polynomial_xy(S, coefficient, i+1))
        return shares

    def reshare_GroupA_shares(self, share):
        reshare_A = []
        for i in range(self.size_B):
            reshare_A.append(self.compute_polynomial(share, i+1))
        return reshare_A

    def get_GroupB_shares(self, reshare_A):
        shares_B = []
        for i in range(self.size_B):
            share_Bi = []
            for j in range(self.size_A):
                share_Bi.append(reshare_A[j][i])
            shares_B.append(share_Bi)
        return shares_B
    
    def generate_new_polynomial(self):
        res = [None] * (self.threshold+1)
        res[0] = 0
        for i in range(1, self.threshold+1):
            res[i] = group.init(ZR, int(random.randrange(1000)))
        return res


    def recover_secret(self, shares):
        points_index, points_value = [], []
        for i in range(self.threshold+1):
            points_index.append(self.size_A-i)
            points_value.append(shares[self.size_A-1-i])
        l = []
        for i in range(self.threshold+1):
            l.append(self.compute_l(points_index, i))
        recovered_polynomial = []
        for i in range(self.threshold+1):
            tmp = 0
            for j in range(len(l)):
                tmp += int(Fraction(int(l[j]['numerator'][i]) * int(points_value[j]), int(l[j]['denominator'])))
            recovered_polynomial.append(int(tmp))
        return recovered_polynomial

            
    def compute_l(self, points_index, i):
        x_i = points_index[i]
        new_point_index = []
        for i in points_index:
            if i != x_i:
                new_point_index.append(i)
        denominator = 1
        _numerator = np.poly1d([1])
        for i in new_point_index:
            denominator *= x_i - i
            _numerator *= np.poly1d([1, -i])
        numerator = list(np.poly1d(_numerator))
        return {'numerator': numerator[::-1], 'denominator':denominator}

    def update_polynomial(self, shares_Bi, new_polynomial):
        updated_polynomial = []
        for i in range(len(shares_Bi)):
            updated_polynomial.append(shares_Bi[i] + new_polynomial[i])
        res = []
        for i in range(self.size_B):
            res.append(self.compute_polynomial(updated_polynomial, i+1))
        # (2* threshold + 1) numbers
        return res

    def update(self, B):
        res = []
        for i in range(self.size_A):
            tmp = []
            for j in range(self.size_A):
                tmp.append(B[j][i])
            res.append(self.recover_secret(tmp)[0])
        # (2* threshold + 1) numbers
        return res


